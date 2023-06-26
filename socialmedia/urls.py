"""socialmedia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from socialmediaapp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('homepage',views.homepage, name='homepage'),
    path('user_login',views.user_login, name='user_login'),
    path('user_register',views.user_register, name='user_register'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('logout', views.user_logout, name='logout'),
    path('successfullyregister', views.successfullyregister, name='successfullyregister'),
    path('update_profile/<str:username>/', views.update_profile, name='update_profile'),
    path('passwordupdated', views.passwordupdated, name='passwordupdated'),
    path('search/', views.search_friends, name='search_friends'),
    path('send-request/<int:friend_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept-friend-request/<int:friend_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('friend-requests/', views.view_friend_requests, name='view_friend_requests'),
    path('remove-friend/<int:friend_id>/', views.remove_friend, name='remove_friend'),
    path('friends-list/', views.view_friends_list, name='view_friends_list'),
    path('cancel-friend-request/<int:friend_id>/', views.cancel_friend_request, name='cancel_friend_request'),
    path('create/', views.create_post, name='create_post'),
    path('update/<int:post_id>/', views.update_post, name='post_update'),
    path('delete/<int:post_id>/', views.delete_post, name='post_delete'),
    path('user-post-list/', views.user_post_list, name='user_post_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)