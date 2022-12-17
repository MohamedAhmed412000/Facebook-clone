from django.urls import path
from . import views, views_api

urlpatterns = [
    path('', views.index, name='index'),
    path('error404', views.error404, name='error404'),
    
    # --------- Authentication -----------
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('account/activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('account/confirm/<str:uidb64>/', views.confirm, name='confirm'),
    path('account/reset/', views.reset, name='reset'),

    # --------- Account Data --------------
    path('account/<str:id>/', views.profile, name='profile'),
    path('account/<str:id>/skill/add/', views.add_skill, name="add-skill"),
    path('account/<str:id>/skill/<str:name>/remove/', views.remove_skill, name="remove-skill"),
    path('account/<str:id>/settings/', views.settings_page, name='settings'),

    # ---------- Post Data ----------------
    path('post/add/', views.add_post, name='add-post'),
    path('post/<str:id>/', views.show_post, name='show-post'),
    path('post/<str:id>/like/', views.like_post, name='like-post'),
    path('post/<str:id>/comment/', views.comment_post, name='comment-post'),
    path('post/<str:id>/share/', views.share_post, name='share-post'),
    path('post/<str:id>/edit/', views.edit_post, name='edit-post'),
    path('post/<str:id>/delete/', views.delete_post, name='delete-post'),
    path('post/<str:id>/disable/', views.disable_comments_post, name='disable-comments-post'),

    # ----------- Comment Data -----------------
    path('comment/<str:id>/edit/', views.edit_comment, name='edit-comment'),
    path('comment/<str:id>/delete/', views.delete_comment, name='delete-comment'),
    path('comment/<str:id>/reply/', views.reply_comment, name='reply-comment'),
    
    # ---------------- Search ------------------
    path('search/tags/<str:tag>/', views.search_tag, name='search-tag'),

    

    # --------------- API_DATA --------------
    
]
