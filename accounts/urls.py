from django.urls import path
import django.contrib.auth.views as auth_views
from . import views

urlpatterns = [
    path('sign-in/', auth_views.LoginView.as_view(template_name="account/login.html"), name='sign_in'),
    path('sign-up/', views.sign_up_user, name='sign_up'),
    path('sign-out/', auth_views.LogoutView.as_view(template_name="account/logged_out.html"), name='sign_out'),
    path('password/change/', auth_views.PasswordChangeView.as_view(template_name="account/password_change_form.html"),
         name='change_password'),
    path('password/change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name="account/password_change_done.html"), name='password_change_done'),
    path('password/reset/', auth_views.PasswordResetView.as_view(
        template_name="account/password_reset_form.html"
    ), name='password_reset'),
    path('password/reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name="account/password_reset_done.html"
    ), name='password_reset_done'),
    path('password/reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="account/password_reset_confirm.html"
    ), name='password_reset_confirm'),
    path('password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="account/password_reset_complete.html"
    ), name='password_reset_complete'),
    path('profile/view', views.view, name='view_profile'),
    path('profile/edit', views.edit, name='edit_profile'),
    path('profile/', views.profile, name='profile'),
]
