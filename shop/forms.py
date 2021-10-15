from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Имя')
    last_name = forms.CharField(max_length=30, required=False, help_text='Фамилия')
    city = forms.CharField(max_length=36, required=False, help_text='Город')
    phone = forms.CharField(max_length=30, required=False, help_text='Телефон')
    information = forms.CharField(help_text='О себе', required=False)
    avatar = forms.ImageField(required=False, help_text='Аватар')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['text']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'


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
