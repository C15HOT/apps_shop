from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    path('', NewsListView.as_view(), name='main'),
    path('login/', AppsLoginView.as_view(), name='login'),
    path('logout/', AppsLogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
    path('app_detail/<str:slug>', AppsDetailView.as_view(), name='app_detail'),
    path('create_app/', CreateAppView.as_view(), name='create_app'),
    path('category/<str:slug>', CategoryDetailView.as_view(), name='category_detail'),
    path('comments/', comments_view, name='comments'),
    path('create-comments/', create_comment, name='comment_create'),
    path('create-child-comment/', create_child_comment, name='comment_child_create'),
    path('apps/', AppsListView.as_view(), name='apps'),
    path('create_news/', NewsAddFormView.as_view(), name='create_news'),
    path('news_detail/<str:slug>', NewsDetailView.as_view(), name='news_detail'),
    path('edit_news/<str:slug>', NewsEditFormView.as_view(), name='edit_news'),
    path('apps_list/', AppsListView.as_view(), name='apps_list'),
    path('info/', InformationView.as_view(), name='information'),
    path('about/', AboutView.as_view(), name='about'),
    path('del_app/<str:slug>/', AppsDelView.as_view(), name='del_app'),
    path('del_news/<str:slug>/', NewsDelView.as_view(), name='del_news'),
    path('profiles/', ProfileListView.as_view(), name='profiles'),
    path('profiles_detail/<str:slug>', ProfileDetailView.as_view(), name='profile_detail'),
    path('edit_profiles/<str:slug>', ProfileEditFormView.as_view(), name='edit_profile'),
    path('edit_app/<str:slug>', AppEditFormView.as_view(), name='edit_app'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)