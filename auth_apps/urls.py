################ Author: https://github.com/pemochamdev #####################

from django.urls import path
from django.contrib.auth import views as auth_views

from auth_apps import views

urlpatterns = [
    # from authy.views
    path('signup/', views.sign_up, name='sign-up'),
    path('profile/<username>/', views.profile, name='profile'),
    path('profile/', views.edit_profile, name='edit-profile'),
    path('password-change/', views.PasswordChange, name='password-change'),
    path('password-change/done/', views.PasswordChangeDone, name='password_change_done'),
    

    # from contrib.auth.views
    path('login/', auth_views.LoginView.as_view(), name='login'),    
    path('log-out/', auth_views.LogoutView.as_view(), name='log-out'),
    path('passwordreset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('passwordreset/done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('passwordreset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/reset/complete', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    

]
