from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, UserDetailView, UserUpdateView, EmailConfirmationSentView, \
    UserConfirmEmailView, EmailConfirmedView, EmailConfirmationFailedView, PasswordRecoveryView, UserListView, \
    block_user, LoginView, logout_user, verify_email

app_name = UsersConfig.name

urlpatterns = [
    path('',  LoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserDetailView.as_view(), name='profile'),
    path('profile/edit/', UserUpdateView.as_view(), name='profile_edit'),
    path('email-confirmation-sent/', EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('confirm-email/<str:uidb64>/<str:token>/', UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email-confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('confirm-email-failed/', EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),
    path('password_recovery/', PasswordRecoveryView.as_view(), name='password_recovery'),
    path('list/', UserListView.as_view(), name='users_list'),
    path('verify_email/<str:uidb64>/<str:token>/', verify_email, name='verify_email'),
    path('block_user/<int:pk>', block_user, name='block_user'),
]