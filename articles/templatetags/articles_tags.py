from django import template
register = template.Library()


# @register.inclusion_tag('articles/create_comment.html', name="create_comment_form", takes_context=True)
# def create_comment_form(context, id):
#     """
#     Commenter un article
#
#     L'utilisateur doit entrer un pseudo s'il n'est pas connecté
#     """
#     article = get_object_or_404(Article, pk=id)
#     request = context['request']
#     user = request.user
#
#     if request.method == 'POST':
#         form = CreateCommentForm(request.POST, request=request)
#
#         if form.is_valid():
#             author = form.cleaned_data['author']
#             content = form.cleaned_data['content']
#
#             if user.is_authenticated():
#                 author = user.username
#
#             # sauvegarde du commentaire
#             commentaire = Commentaire(content=content, author=author, article=article)
#             commentaire.save()
#
#             return {'form': form, 'user': user}
#
#     else:
#         form = CreateCommentForm(request=request)
#
#     return {'form': form, 'user': user}
