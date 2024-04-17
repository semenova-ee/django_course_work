from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView as BaseLoginView, PasswordResetConfirmView, PasswordResetView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import render, redirect

from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, TemplateView, FormView, ListView

from config import settings
from users.forms import UserRegisterForm, UserForm, PasswordRecoveryForm
from users.models import User
from users.mixins import UserIsNotAuthenticated


class LoginView(BaseLoginView):
    template_name = 'users/authenticate/login.html'

# def login_user(request):
#        if request.method == "POST":
#            email = request.POST['email']
#            password = request.POST['password']
#            user = authenticate(request, email=email, password=password)
#            if user is not None:
#                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#                messages.success(request, "Welcome!")
#                return redirect('mailing:index')
#            else:
#                messages.success(request, "There Was An Error Logging In, Try Again...")
#                return redirect('users:login')
#
#        else:
#            return render(request, 'users/authenticate/login.html', {})
#

def logout_user(request):
    logout(request)
    messages.success(request, ("You Were Logged Out!"))
    return redirect('mailing:index')




class RegisterView(UserIsNotAuthenticated, CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/authenticate/register_user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True
        user.save()
        # Функционал для отправки письма и генерации токена
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse_lazy('users:confirm_email', kwargs={'uidb64': uid, 'token': token})
        current_site = Site.objects.get_current().domain
        send_mail(
            'Mailing Service: Подтвердите свой электронный адрес, перейдя по ссылке',
            f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты: http://{current_site}{activation_url}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        print(f'Email sent {user.email}')
        return redirect('users:email_confirmation_sent')


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user/user_detail.html'


    def get_object(self, queryset=None):
        return self.request.user


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserForm
    template_name = 'users/user/user_form.html'


    def get_object(self, queryset=None):
        return self.request.user


class UserConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('users:email_confirmed')
        else:
            return redirect('users:email_confirmation_failed')


class EmailConfirmationSentView(TemplateView):
    template_name = 'users/email/email_confirmed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Письмо активации отправлено'
        return context


class EmailConfirmedView(TemplateView):
    template_name = 'users/email/email_confirmed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес активирован'
        return context


class EmailConfirmationFailedView(TemplateView):
    template_name = 'users/email/email_confirmation_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес не активирован'
        return context


class PasswordRecoveryView(FormView):
    template_name = 'users/pass/password_recovery.html'
    form_class = PasswordRecoveryForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = User.objects.get(email=email)
        length = 12
        alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        password = get_random_string(length, alphabet)
        user.set_password(password)
        user.save()
        subject = 'Password Recovery'
        message = f'Your new password: {password}'
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return super().form_valid(form)


class UserListView(PermissionRequiredMixin, ListView):
    model = User
    permission_required = 'users.view_user'
    success_url = reverse_lazy('users:users_list')
    template_name = 'users/user/user_list.html'



    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_superuser:
            queryset = super().get_queryset()
        else:
            queryset = super().get_queryset().filter(is_superuser=False, is_staff=False)
        return queryset


@permission_required('users.view_user')
def block_user(self, pk):
    user = User.objects.get(pk=pk)
    user.is_active = {user.is_active: False,
                          not user.is_active: True}[True]
    user.save()
    return redirect(reverse('users:users_list'))