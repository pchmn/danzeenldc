import json
import os
from datetime import datetime, timedelta
import collections

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.views.generic.edit import UpdateView
from django.core.paginator import Paginator, EmptyPage
from django.contrib import messages

from articles.models import Article, Commentaire
from articles.forms import CreateArticleForm, CreateCommentForm
from articles.utils import bleach_html


@user_passes_test(lambda u: u.has_perm('articles.add_article'))
def create_article(request):
    """
    Création d'un article

    Il faut être connecté et avoir les bons droits
    """
    user = request.user

    if request.method == 'POST':
        form = CreateArticleForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            intro = form.cleaned_data['intro']
            content = form.cleaned_data['content']

            # sauvegarde de l'article
            article = Article(title=title, intro=intro, content=content, author=user)
            article.save()

            # on redirige vers l'article créé
            return redirect("get_article", slug=article.slug)

    else:
        form = CreateArticleForm()

    return render(request, "articles/create_article.html", locals())


class UpdateArticle(UpdateView):
    """
    Modification d'un article

    L'utilisateur qui veut modifier l'article doit en être l'auteur
    """
    model = Article
    fields = ['title', 'intro', 'content']
    template_name = "articles/update_article.html"

    # on vérifie que l'user connecté est bien l'auteur de l'article
    def dispatch(self, request, *args, **kwargs):
        if request.user != self.get_object().author:
            raise PermissionDenied()
        return super(UpdateArticle, self).dispatch(request, *args, **kwargs)

    # récupération du bon article selon le slug
    def get_object(self):
        article = Article.objects.get(slug=self.kwargs['slug'])
        article.content = bleach_html(article.content)
        article.content = article.content.replace('"', '\\"')
        print(article.content)
        return article

    # on redirige vers l'article modifié en cas de succès
    def get_success_url(self):
        messages.success(self.request, 'Article modifié !', extra_tags='done')
        return reverse_lazy("get_article", kwargs={'slug': self.object.slug})


def delete_article(request, id):
    """
    Suppression d'un article selon un id
    """
    article = get_object_or_404(Article, pk=id)
    user = request.user

    # on vérifie que l'utilisateur a les bons droits
    # et qu'il est l'auteur de l'article
    if not user.is_staff or user != article.author:
        raise PermissionDenied()

    # suppression de l'article
    article.delete()

    return redirect("get_articles")


# class GetArticlesList(ListView):
#     """
#     Récupération des articles par page
#     10 articles par page
#     """
#     model = Article
#     template_name = "articles/articles_list.html"
#     context_object_name = "articles"
#     paginate_by = 10
#     # page name : page_obj
#
#     def get_queryset(self):
#         order = self.request.GET.get('order', '-date')
#         print(order)
#         if order != "-date" and order != "-views" and order != "-score":
#             order = "-date"
#         print(order)
#         return Article.objects.order_by(order)


def get_articles(request, page=1):
    """
    Récupération des articles par page
    10 articles par page
    """
    # récupération du filtre
    order = request.GET.get('order', '-date')
    if order != "-date" and order != "-views" and order != "-score":
        order = "-date"

    articles_list = Article.objects.order_by(order)
    paginator = Paginator(articles_list, 10)

    try:
        articles = paginator.page(page)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    # récupération classement ligue 1
    f1 = os.path.join(os.path.dirname(__file__), 'json/ranking_ligue1.json')
    ranking = json.load(open(f1), object_pairs_hook=collections.OrderedDict)

    # récupération du dernier résultat et du prochain match de Rennes
    f2 = os.path.join(os.path.dirname(__file__), 'json/last_next_match.json')
    last_next_match = json.load(open(f2))

    last_result = last_next_match['last_result']
    last_result['date'] = datetime.strptime(last_result['date'], "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=1)
    next_match = last_next_match['next_match']
    next_match['date'] = datetime.strptime(next_match['date'], "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=1)

    return render(request, "articles/articles_list.html", locals())


def get_article(request, slug):
    """
    Récupération d'un article selon un slug

    Le nombre de vues est augmenté à chaque fois qu'un
    utilisateur accède la première fois à l'article

    Lors de cette première visite un cookie est placé
    Le cookie est une liste qui correspond aux id des articles
    que l'utilisateur a vu
    """
    article = get_object_or_404(Article, slug=slug)
    # derniers articles pour les afficher
    last_articles = Article.objects.all().exclude(slug=article.slug).order_by('-date')[:5]
    # variables utiles pour le vote
    votes_article = {}
    already_voted = False
    id_article_texte = str(article.id)
    form_success = False

    # récupération des commentaires de l'article
    # 10 par page
    comments_list = Commentaire.objects.filter(article=article).order_by('-date')
    paginator = Paginator(comments_list, 10)

    page_comments = request.GET.get('page_comments', '1')
    int(page_comments)

    try:
        comments = paginator.page(page_comments)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    # on test si l'utilisateur a déjà voté pour l'article
    # afin de masqué un des boutons de vote si c'est le cas
    user = request.user
    if user.is_authenticated():
        votes_article = user.profile.votes_articles
    else:
        if 'cookie_votes_article' in request.session:
            votes_article = request.session['cookie_votes_article']

    if id_article_texte in votes_article:
        opinion = votes_article[id_article_texte]
        already_voted = True

    # vérifie si l'utilisateur a déjà vu l'article
    # fonction annexe
    set_cookie_view_article(request, article)

    # traitement du formulaire de commentaire
    # fonction annexe
    response = create_comment_form(request, article)
    if response['send']:
        if response['saved']:
            messages.success(request, 'Commentaire posté !', extra_tags='done')
            return redirect("get_article", article.slug)
        else:
            form = response['form']
            messages.error(request, 'Erreur dans le formulaire', extra_tags='report_problem')

    return render(request, "articles/article.html", locals())


def set_cookie_view_article(request, article):
    """
    Fonction annexe permettant de tester
    le cookie pour les vues d'un article
    """
    views_article = []
    user = request.user

    # si l'utilisateur est connecté, on regarde s'il a deja vu l'article
    if user.is_authenticated():
        views_article = user.profile.views_articles
        if str(article.id) not in views_article:
            article.views += 1
            article.save()
            views_article[article.id] = ""
            user.profile.views_articles = views_article
            user.profile.save()

    else:
        # on test si l'utilisateur avait déjà vu cet article
        if 'cookie_views_article' in request.session:
            views_article = request.session['cookie_views_article']
            # si l'utilisateur n'avait pas vu cet article
            if article.id not in views_article:
                article.views += 1
                article.save()
                views_article.append(article.id)
        else:
            article.views += 1
            article.save()
            views_article.append(article.id)

        # on met à jour le cookie
        request.session['cookie_views_article'] = views_article


def create_comment_form(request, article):
    """
    Fonction annexe qui gère le post de commentaire

    L'utilisateur doit entrer un pseudo s'il n'est pas connecté
    """
    user = request.user
    result = {}

    if request.method == 'POST':
        form = CreateCommentForm(request.POST, request=request)
        result['send'] = True

        if form.is_valid():
            author = form.cleaned_data['author']
            content = form.cleaned_data['content']

            if user.is_authenticated():
                author = user.username

            # sauvegarde du commentaire
            commentaire = Commentaire(content=content, author=author, article=article)
            commentaire.save()

            result['saved'] = True
        else:
            result['saved'] = False

    else:
        form = CreateCommentForm(request=request)
        result['send'] = False

    result['form'] = form

    return result



