import json
import os

import datetime

import collections
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.http import Http404, JsonResponse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage
from django.contrib import messages

from articles.models import Article, Commentaire
from articles.forms import CreateArticleForm, CreateCommentForm


@login_required()
def create_article(request):
    """
    Création d'un article

    Il faut être connecté et avoir les bons droits
    """
    user = request.user

    # vérification des bons droits
    if not user.is_staff:
        raise PermissionDenied()

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
    last_result['date'] = datetime.datetime.strptime(last_result['date'], "%Y-%m-%dT%H:%M:%SZ")
    next_match = last_next_match['next_match']
    next_match['date'] = datetime.datetime.strptime(next_match['date'], "%Y-%m-%dT%H:%M:%SZ")

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
    if 'cookie_votes_article' in request.session:
        cookie_votes_article = request.session['cookie_votes_article']
        if id_article_texte in cookie_votes_article:
            opinion = cookie_votes_article[id_article_texte]
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
        if self.request.user != self.get_object().author:
            raise PermissionDenied()
        return super(UpdateArticle, self).dispatch(request, *args, **kwargs)

    # récupération du bon article selon le slug
    def get_object(self):
        return Article.objects.get(slug=self.kwargs['slug'])

    # on redirige vers l'article modifié en cas de succès
    def get_success_url(self):
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


def vote_article(request, id_article, opinion):
    """
    Voter pour un article

    Lors du vote, un cookie est placé pour éviter qu'un même personne
    puisse voter plusieurs fois.
    Avant de voter on teste donc la présence du cookie
    Le cookie est un dictionnaire avec en clé l'id de l'article et en valeur le vote
    """
    article = get_object_or_404(Article, pk=id_article)
    already_voted = False
    cookie_votes_article = {}
    id_article_texte = str(id_article)

    # test de la présence du cookie
    if 'cookie_votes_article' in request.session:
        cookie_votes_article = request.session['cookie_votes_article']
        # on vérifie que l'utilisateur n'avait pas déjà effectué ce vote
        if id_article_texte in cookie_votes_article and opinion == cookie_votes_article[id_article_texte]:
            return JsonResponse({
                'article': article.title,
                'vote': 'déjà voté',
                'likes': article.likes,
                'dislikes': article.dislikes
            })
        already_voted = True

    # ajout du vote
    if opinion == "like_article":
        article.likes += 1
        # si l'utilisateur avait déjà voté on rectifie le nb de dislikes
        if already_voted and article.dislikes > 0:
            article.dislikes -= 1

    elif opinion == "dislike_article":
        article.dislikes += 1
        # si l'utilisateur avait déjà voté on rectifie le nb de likes
        if already_voted and article.likes > 0:
            article.likes -= 1

    else:
        return JsonResponse({
            'article': article.title,
            'error': 'mauvais paramètre',
            'vote': 'déjà voté',
            'likes': article.likes,
            'dislikes': article.dislikes
        })

    article.save()
    # ajout du vote dans le dictionnaire du cookie
    cookie_votes_article[id_article_texte] = opinion
    # on met à jour le cookie
    request.session['cookie_votes_article'] = cookie_votes_article

    return JsonResponse({
        'article': article.title,
        'vote': opinion,
        'likes': article.likes,
        'dislikes': article.dislikes
    })


def vote_comment(request, id_comment, opinion):
    """
    Voter pour un commentaire

    Lors du vote, un cookie est placé pour éviter qu'un même personne
    puisse voter plusieurs fois.
    Avant de voter on teste donc la présence du cookie
    Le cookie est un dictionnaire avec en clé l'id du commentaire et en valeur le vote
    """
    commentaire = get_object_or_404(Commentaire, pk=id_comment)
    article = get_object_or_404(Article, pk=commentaire.article.id)
    already_voted = False
    cookie_votes_comment = {}
    id_comment_texte = str(id_comment)

    # test de la présence du cookie
    if 'cookie_votes_comment' in request.session:
        cookie_votes_comment = request.session['cookie_votes_comment']
        # on vérifie que l'utilisateur n'avait pas déjà effectué ce vote
        if id_comment_texte in cookie_votes_comment and opinion == cookie_votes_comment[id_comment_texte]:
            return JsonResponse({
                'comment': commentaire.id,
                'vote': 'déjà voté',
                'likes': commentaire.likes,
                'dislikes': commentaire.dislikes,
                'score': commentaire.score
            })
        already_voted = True

    # ajout du vote
    if opinion == "like_comment":
        commentaire.likes += 1
        if already_voted and commentaire.dislikes > 0:
            commentaire.dislikes -= 1
    elif opinion == "dislike_comment":
        commentaire.dislikes += 1
        if already_voted and commentaire.likes > 0 and commentaire.score > 0:
            commentaire.likes -= 1
    else:
        raise Http404("Mauvais paramètre")

    commentaire.save()
    # ajout du vote dans le dictionnaire du cookie
    cookie_votes_comment[id_comment_texte] = opinion
    # on met le cookie
    request.session['cookie_votes_comment'] = cookie_votes_comment

    return JsonResponse({
        'comment': commentaire.id,
        'vote': opinion,
        'likes': commentaire.likes,
        'dislikes': commentaire.dislikes,
        'score': commentaire.score
    })



