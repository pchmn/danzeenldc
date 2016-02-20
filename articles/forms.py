from django import forms
from articles.models import Article, Commentaire
from django.contrib.auth.models import User


class CreateArticleForm(forms.ModelForm):
    title = forms.CharField(error_messages={'required': "Votre titre est vide"})
    intro = forms.CharField(error_messages={'required': "Votre intro est vide"})
    content = forms.CharField(error_messages={'required': "Votre article est vide"})

    class Meta:
        model = Article
        fields = ["title", "intro", "content"]


class CreateCommentForm(forms.Form):
    author = forms.CharField(widget=forms.TextInput, required=False, label="Pseudo")
    content = forms.CharField(widget=forms.Textarea, label="Commentaire", error_messages={'required': "Votre commentaire est vide"})

    # permet de récupérer l'objet request
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CreateCommentForm, self).__init__(*args, **kwargs)

    def clean_author(self):
        author = self.cleaned_data.get('author')
        if User.objects.filter(username=author).exists():
            raise forms.ValidationError("Pseudo déjà utilisé par un membre du site")
        if author == "":
            author = "Anonyme"
        return author
