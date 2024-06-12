from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Post, Komentarz

class UserRegisterForm(UserCreationForm):
    imie = forms.CharField(max_length=30)
    nazwisko = forms.CharField(max_length=30)
    wiek = forms.IntegerField()

    class Meta:
        model = CustomUser
        fields = ['username', 'imie', 'nazwisko', 'wiek', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['imie', 'nazwisko', 'wiek']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['tytul', 'tresc']

class KomentarzForm(forms.ModelForm):
    class Meta:
        model = Komentarz
        fields = ['tresc']
