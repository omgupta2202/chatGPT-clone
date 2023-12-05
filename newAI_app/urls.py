from django.urls import path
from . import views
# from django.contrib.auth.views import LoginView
urlpatterns = [
    path('', views.signin_view, name="signin-page"),
    path('sign-up', views.signup_view, name="signup-page"),
    path('logout', views.logout_view, name="logout-page"),
    path('home', views.index, name="home-page"),
    # path('livechat', views.chatgptView, name="livechat-page"),
]
