from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
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
    paginate_by = 18


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


class RegisterView(View):

    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    @transaction.atomic()
    def post(self, request):

        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            phone = form.cleaned_data.get('phone')
            city = form.cleaned_data.get('city')
            email = form.cleaned_data.get('email')
            information = form.cleaned_data.get('information')
            avatar = form.cleaned_data.get('avatar')
            position = form.cleaned_data.get('position')
            if avatar:
                Profile.objects.create(
                    user=user,
                    city=city,
                    phone=phone,
                    slug=user.username,
                    avatar=avatar,
                    information=information,
                    email=email,
                    position=position,
                )
            else:
                Profile.objects.create(
                    user=user,
                    city=city,
                    phone=phone,
                    slug=user.username,

                    information=information,
                    email=email,
                    position=position,
                )

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')

        return render(request, 'register.html', {'form': form})


class AppsDetailView(generic.DetailView):
    model = App
    context_object_name = 'app'
    template_name = 'apps_detail.html'

    def post(self, request, pk):
        print(request)
        if request.POST.get('download'):
            app = self.get_object()
            print(app.download_count)
            app.download_count += 1
            print(app.download_count)
            app.save()
            return redirect(reverse('app_detail', args=[app.slug]))


    def get_context_data(self, **kwargs):
        context = super(AppsDetailView, self).get_context_data(**kwargs)

        context['files'] = self.object.screenshots.all()

        return context

class AppEditFormView(View):

    def get(self, request, slug):
        app = App.objects.get(slug=slug)
        app_form = AppForm(instance=app)
        screens = app.screenshots.all()

        screenshots_form = ScreenshotsForm()
        return render(request, 'edit_app.html', context={'app_form': app_form, 'slug': slug, 'screenshots': screens,
                                                         'screenshots_form': screenshots_form})

    def post(self, request, slug):
        app = App.objects.get(slug=slug)
        app_form = AppForm(request.POST, request.FILES, instance=app)
        screenshots_form = ScreenshotsForm(request.POST, request.FILES)
        files = request.FILES.getlist('files')
        if app_form.is_valid() and screenshots_form.is_valid():
            app.save()
            for f in files:
                instance = ScreenshotsApp(files=f, app=app)
                instance.save()
            return redirect('app_detail', slug=slug)
        return render(request, 'edit_app.html', context={'app_form': app_form, 'slug': slug,
                                                         'screenshots_form':screenshots_form})


class CreateAppView(View):

    def get(self, request):
        app_form = AppForm()
        screenshots_form = ScreenshotsForm()

        return render(request, 'create_app.html', context={'app_form': app_form, 'screenshots_form':screenshots_form})

    @transaction.atomic()
    def post(self, request):

        app_form = AppForm(request.POST, request.FILES)
        screenshots_form = ScreenshotsForm(request.POST, request.FILES)

        files = request.FILES.getlist('files')
        slug = slugify(request.POST['title']+'_абс')
        # Нужно добавлять проверку на уникальность или сразу делать уникальным
        if app_form.is_valid() and screenshots_form.is_valid():
            app = App.objects.create(**app_form.cleaned_data, slug=slug, user_id=request.user.id)

            for f in files:
                instance = ScreenshotsApp(files=f, app=app)
                instance.save()

            return HttpResponseRedirect('/')
        return render(request, 'create_app.html', context={'app_form': app_form, 'screenshots_form':screenshots_form})


class NewsListView(generic.ListView):
    model = News
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    queryset = News.objects.select_related('user__profiles').all()
    paginate_by = 6


class NewsDetailView(generic.DetailView):
    model = News
    template_name = 'news_detail.html'
    context_object_name = 'news'
    queryset = News.objects.select_related('user__profiles').all()


class NewsAddFormView(View):

    def get(self, request):
        news_form = NewsForm()
        return render(request, 'create_news.html', context={'news_form': news_form})

    def post(self, request):
        news_form = NewsForm(request.POST, request.FILES)
        print(request.POST['title'])
        slug = slugify(request.POST['title']+'_абс')
        print(slug)

        # Нужно добавлять проверку на уникальность или сразу делать уникальным

        if news_form.is_valid():
            News.objects.create(**news_form.cleaned_data, slug=slug, user_id=request.user.id)
            return HttpResponseRedirect('/')
        return render(request, 'create_news.html', context={'news_form': news_form})


class NewsEditFormView(View):

    def get(self, request, slug):
        news = News.objects.get(slug=slug)
        news_form = NewsForm(instance=news)
        return render(request, 'edit_news.html', context={'news_form': news_form, 'slug': slug})

    def post(self, request, slug):
        news = News.objects.get(slug=slug)
        news_form = NewsForm(request.POST, request.FILES,  instance=news)
        if news_form.is_valid():
            news.save()
            return redirect('news_detail', slug=slug)
        return render(request, 'edit_news.html', context={'news_form': news_form, 'slug': slug})


class ProfileListView(generic.ListView):
    model = Profile
    template_name = 'profile_list.html'
    context_object_name = 'profile_list'
    queryset = Profile.objects.select_related('user').all()


class ProfileDetailView(generic.DetailView):
    model = Profile
    template_name = 'profile_detail.html'
    context_object_name = 'profile'
    queryset = Profile.objects.select_related('user').all()


class ProfileEditFormView(View):

    def get(self, request, slug):
        profile = Profile.objects.get(slug=slug)
        profile_form = ProfileForm(instance=profile)
        return render(request, 'edit_profile.html', context={'profile_form': profile_form, 'slug': slug})

    def post(self, request, slug):
        profile = Profile.objects.get(slug=slug)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile.save()
            return redirect('profile_detail', slug=slug)
        return render(request, 'edit_profile.html', context={'profile_form': profile_form, 'slug': slug})



class InformationView(View):
    def get(self, request):
        return render(request, 'information.html')


class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')


class NewsDelView(View):
    def get(self, request, slug):
        news = News.objects.get(slug=slug)
        news.delete()
        return redirect('main')


class AppsDelView(View):
    def get(self, request, slug):
        app = App.objects.get(slug=slug)
        app.delete()
        return redirect('apps_list')


class DownloadFileView(View):

    def get(self, request, slug):
        app = App.objects.get(slug=slug)
        app.download_count += 1
        app.save(update_fields=['download_count'])
        return HttpResponseRedirect(app.file.url)


class SearchAppsView(generic.ListView):
    model = App
    template_name = 'search_app.html'

    def get_queryset(self):

        query = self.request.GET.get('q')
        object_list = App.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        return object_list

