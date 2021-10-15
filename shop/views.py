from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View, generic
from transliterate import slugify
from .forms import RegisterForm
from .models import *
from .forms import *
from .utils import create_comments_tree
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

def comments_view(request):
    comments = App.objects.first().comments.all()
    result = create_comments_tree(comments)
    comment_form = CommentForm(request.POST or None)
    return render(request, 'comments.html', {'comments': result, 'comment_form': comment_form})


def create_comment(request):
    comment_form = CommentForm(request.POST or None)
    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.user = request.user
        new_comment.text = comment_form.cleaned_data['text']
        new_comment.content_type = ContentType.objects.get(model='app')
        new_comment.object_id = 1
        new_comment.parent = None
        new_comment.is_child = False
        new_comment.save()
    return HttpResponseRedirect('/comments')

@transaction.atomic
def create_child_comment(request):
     user_name = request.POST.get('user')
     current_id = request.POST.get('id')
     text = request.POST.get('text')
     user = User.objects.get(user_name=user_name)
     content_type = ContentType.objects.get(model='app')
     parent = Comments.objects.get(id=int(current_id))
     is_child = False if not parent else True
     Comments.objects.create(
         user=user, text=text, content_type=content_type, object_id=1,
         parent=parent, is_child=is_child
     )
     comments = App.objects.first().comments.all()
     comments_list = create_comments_tree(comments)
     return render(request, 'comments.html', {'comments': comments_list})

class AppsListView(generic.ListView):
    model = App
    template_name = 'apps_list.html'
    context_object_name = 'apps_list'
    queryset = App.objects.all()

    def get_context_data(self, **kwargs):
        context = super(AppsListView, self).get_context_data(**kwargs)

        context['categories'] = Category.objects.all()

        return context


class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category'



class AppsLoginView(LoginView):
    template_name = 'login.html'


class AppsLogoutView(LogoutView):
    next_page = '/'


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone = form.cleaned_data.get('phone')
            city = form.cleaned_data.get('city')
            Profile.objects.create(
                user=user,
                city=city,
                phone=phone,
            )

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


class AppsDetailView(generic.DetailView):
    model = App
    context_object_name = 'app'
    template_name = 'apps_detail.html'


class CreateAppView(View):

    def get(self, request):
        app_form = AppForm

        return render(request, 'create_app.html', context={'app_form': app_form})

    def post(self, request):
        app_form = AppForm(request.POST, request.FILES)

        slug = slugify(request.POST['title'])
        # Нужно добавлять проверку на уникальность или сразу делать уникальным
        if app_form.is_valid():
            App.objects.create(**app_form.cleaned_data, slug=slug, user_id=request.user.id)


            return HttpResponseRedirect('/')
        return render(request, 'create_app.html', context={'app_form': app_form})

