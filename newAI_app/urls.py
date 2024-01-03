from django.urls import path
from . import views
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
urlpatterns = [
    path('', views.signin_view, name="signin-page"),
    path('sign-up', views.signup_view, name="signup-page"),
    path('logout', views.logout_view, name="logout"),
    path('home', views.index, name="home"),
    path('delete-chat/<int:chat_id>/', views.delete_chat, name='delete_chat'),
    path('get-conversation/', views.get_conversation, name='get_conversation'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    
    # path('password-reset/', PasswordResetView.as_view(template_name='newAI_app/password_reset.html'),name='password-reset'),
    # path('password-reset/done/', PasswordResetDoneView.as_view(template_name='newAI_app/password_reset_done.html'),name='password_reset_done'),
    # path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='newAI_app/password_reset_confirm.html'),name='password_reset_confirm'),
    # path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='newAI_app/password_reset_complete.html'),name='password_reset_complete'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
