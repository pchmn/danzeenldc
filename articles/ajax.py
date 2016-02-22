from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from articles.models import Article, Commentaire


def vote_article(request, id_article):
    """
    Voter pour un article

    Lors du vote, un cookie est placé pour éviter qu'un même personne
    puisse voter plusieurs fois.
    Avant de voter on teste donc la présence du cookie
    Le cookie est un dictionnaire avec en clé l'id de l'article et en valeur le vote
    """
    article = get_object_or_404(Article, pk=id_article)
    already_voted = False
    votes_article = {}
    id_article_texte = str(id_article)
    user = request.user

    opinion = request.GET.get('opinion', '')

    # si l'utilisateur est connecté
    if user.is_authenticated():
        votes_article = user.profile.votes_articles

    else:
        # test de la présence du cookie
        if 'cookie_votes_article' in request.session:
            votes_article = request.session['cookie_votes_article']

    # on vérifie si l'utilisateur a déjà voté pour cet article
    if id_article_texte in votes_article:
        already_voted = True
        # on vérifie que l'utilisateur n'avait pas déjà effectué ce vote
        if opinion == votes_article[id_article_texte]:
            return JsonResponse({
                'article': article.title,
                'vote': 'déjà voté',
                'likes': article.likes,
                'dislikes': article.dislikes
            })

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
            'likes': article.likes,
            'dislikes': article.dislikes
        })

    article.save()
    # ajout du vote dans le dictionnaire du cookie
    votes_article[id_article_texte] = opinion
    # on met à jour le cookie
    if user.is_authenticated():
        user.profile.votes_articles = votes_article
        user.profile.save()
    else:
        request.session['cookie_votes_article'] = votes_article

    return JsonResponse({
        'article': article.title,
        'vote': opinion,
        'likes': article.likes,
        'dislikes': article.dislikes
    })


def vote_comment(request, id_comment):
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
    votes_comment = {}
    id_comment_texte = str(id_comment)
    user = request.user

    opinion = request.GET.get('opinion', '')

    # si l'utilisateur est connecté
    if user.is_authenticated():
        votes_comment = user.profile.votes_comments

    # test de la présence du cookie
    if 'cookie_votes_comment' in request.session:
        votes_comment = request.session['cookie_votes_comment']

    # on vérifie si l'utilisateur a deja voté pour cet article
    if id_comment_texte in votes_comment:
        already_voted = True
        # on vérifie que l'utilisateur n'avait pas déjà effectué ce vote
        if opinion == votes_comment[id_comment_texte]:
            return JsonResponse({
                'comment': commentaire.id,
                'vote': 'déjà voté',
                'likes': commentaire.likes,
                'dislikes': commentaire.dislikes,
                'score': commentaire.score
            })

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
        return JsonResponse({
            'commentaire': commentaire.title,
            'error': 'mauvais paramètre',
            'likes': commentaire.likes,
            'dislikes': commentaire.dislikes
        })

    commentaire.save()
    # ajout du vote dans le dictionnaire du cookie
    votes_comment[id_comment_texte] = opinion
    # on met le cookie
    if user.is_authenticated():
        user.profile.votes_comments = votes_comment
        user.profile.save()
    else:
        request.session['cookie_votes_comment'] = votes_comment

    return JsonResponse({
        'comment': commentaire.id,
        'vote': opinion,
        'likes': commentaire.likes,
        'dislikes': commentaire.dislikes,
        'score': commentaire.score
    })