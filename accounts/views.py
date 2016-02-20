from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView
from accounts.forms import CreateUserForm, LoginForm, UpdatePasswordForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


class CreateUser(CreateView):
    """
    Création d'un utilisateur
    Il n'a aucun droit de base
    Son compte est activé lors de la création
    """
    model = User
    form_class = CreateUserForm
    template_name = 'accounts/create_user.html'

    # on redirige vers l'article modifié en cas de succès
    def get_success_url(self):
        messages.success(self.request, 'Inscription validée !', extra_tags='done')
        return reverse_lazy("login")


def login_user(request):
    """
    Gère la connexion d'un utilisateur
    Vérifie que la combinaison pseudo/mot de passe est bonne
    Et que le compte est actif
    """
    next = request.GET.get('next', "")

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            # vérification bons pseudo/mdp
            if user:
                if user.is_active:
                    # si le compte est actif, l'utilisateur est connecté
                    login(request, user)

                    #
                    if next == "":
                        return redirect("get_articles")
                    else:
                        return HttpResponseRedirect(next)
                else:
                    user = None
                    error = "Ton compte n'est pas actif"
            else:
                error = "Mauvais pseudo et/ou mot de passe"

    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', locals())


def logout_user(request):
    """
    Déconnexion de l'utilisateur
    """
    logout(request)
    return redirect('get_articles')


def get_profile(request, username):
    """
    Récupération du profil d'un utilisateur selon son pseudo
    """
    user = get_object_or_404(User, username=username)

    return render(request, 'accounts/profile.html', locals())


@login_required()
def change_password(request):
    """
    Modification du mot de passe d'un utilisateur
    L'utilisateur doit être connecté
    """
    if request.method == 'POST':
        form = UpdatePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Commentaire posté !', extra_tags='done')
            return redirect("get_articles")

    else:
        form = UpdatePasswordForm(user=request.user)

    return render(request, 'accounts/change_password.html', locals())
