
from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # path("newPost", views.newPostForUser),
    path("profile/<str:userName>", views.profilePage, name="profile"),
    path("following/<str:userName>", views.following, name="following"),
    # path("saveEditedTweet/<int:post_id>", views.saveEditedTweet, name="saveEditedTweet"),



    #API Route
    path("edit/<int:post_id>", views.editTweet, name="editTweet"),
    
    # #Ajax call
    # re_path(r'^like_post/$', views.likePost, name='likePost'),
    path("like_post/<int:post_id>", views.likePost, name="likePost"),
   


]
