from django.urls import path
from . import views
# from django.contrib.auth.views import LoginView
urlpatterns = [
    path('', views.signin_view, name="signin-page"),
    path('sign-up', views.signup_view, name="signup-page"),
    path('logout', views.logout_view, name="logout"),
    path('home', views.index, name="home"),
    path('delete-chat/<int:chat_id>/', views.delete_chat, name='delete_chat'),
    path('get-conversation/', views.get_conversation, name='get_conversation'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]
