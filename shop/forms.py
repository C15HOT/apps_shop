from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label='Имя', required=False)
    last_name = forms.CharField(max_length=30, label='Фамилия', required=False )
    city = forms.CharField(max_length=36, required=False, label='Город')
    phone = forms.CharField(max_length=30, required=False, label='Телефон')
    information = forms.CharField(label='О себе', required=False)
    avatar = forms.ImageField(required=False, label='Фото профиля')
    email = forms.EmailField(max_length=50, required=True, label='Email')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['text']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('title', 'content', 'image')

class AppForm(forms.ModelForm):
    class Meta:
        model = App
        fields = ('title', 'image', 'description', 'category', 'file')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = [
            'text'
        ]


class ScreenshotsForm(forms.Form):
    files = forms.FileField(label='Скриншоты программы', required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))


