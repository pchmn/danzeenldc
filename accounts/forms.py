import collections

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm


class CreateUserForm(UserCreationForm):

    error_messages = {
        'password_mismatch': "Les deux mot de passes sont différents",
    }
    password1 = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Confirmation mot de passe",
        widget=forms.PasswordInput,
        help_text="Enter the same password as before, for verification.")

    class Meta:
        model = User
        fields = ["username", "email"]
        labels = {
            'username': 'Nom d\'utilisateur',
            'email': 'Adresse email',
        }
        error_messages = {
            'username': {
                'unique': 'Ce nom d\'utilisateur est déjà utilisé'
            }
        }

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required': 'Ce champ est obligatoire'.format(
                fieldname=field.label)}

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé")
        return email

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, label="Nom d'utilisateur")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")


class UpdatePasswordForm(PasswordChangeForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = {
        'password_incorrect': "L'ancien mot de passe n'est pas bon",
        'password_mismatch': "Les deux mot de passes sont différents",
    }

    old_password = forms.CharField(
        label="Ancien mot de passe",
        widget=forms.PasswordInput(attrs={'autofocus': ''}),
    )

    new_password1 = forms.CharField(
        label="Nouveau mot de passe",
        widget=forms.PasswordInput,
    )

    new_password2 = forms.CharField(
        label="Confirmaton nouveau mot de passe",
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required': 'Ce champ est obligatoire'.format(
                fieldname=field.label)}

UpdatePasswordForm.base_fields = collections.OrderedDict(
    (k, UpdatePasswordForm.base_fields[k])
    for k in ['old_password', 'new_password1', 'new_password2']
)