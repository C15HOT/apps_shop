from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    path('', AppsListView.as_view(), name='main'),
    path('login/', AppsLoginView.as_view(), name='login'),
    path('logout/', AppsLogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
    path('app_detail/<str:slug>', AppsDetailView.as_view(), name='app_detail'),
    path('create_app/', CreateAppView.as_view(), name='create_app'),
    path('category/<str:slug>', CategoryDetailView.as_view(), name='category_detail'),
    path('comments/', comments_view, name='comments'),
    path('create-comments/', create_comment, name='comment_create'),
    path('create-child-comment/', create_child_comment, name='comment_child_create')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)