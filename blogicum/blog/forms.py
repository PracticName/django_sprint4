from django import forms
from django.contrib.auth.forms import UserCreationForm

from . models import Post, User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author', 'is_published',)
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'datetime-local'})
        }


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email',)
