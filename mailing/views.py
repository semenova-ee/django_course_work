from random import sample

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from blog.models import Blog
from mailing.forms import MailingForm, ClientForm, MessageForm
from mailing.models import Client, Mailing, Message, MailingLog


class IndexView(TemplateView):
    template_name = 'mailing/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Главная'
        context_data['count_mailing'] = len(Mailing.objects.all())
        active_mailings_count = Mailing.objects.filter(is_active=True).count()
        context_data['active_mailings_count'] = active_mailings_count
        unique_clients_count = Client.objects.filter(is_active=True).distinct().count()
        context_data['unique_clients_count'] = unique_clients_count
        all_posts = list(Blog.objects.filter(is_published=True))
        context_data['random_blog_posts'] = sample(all_posts, min(3, len(all_posts)))
        return context_data


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'mailing/client/client_list.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = "Пользователи"
        return context_data

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.groups.filter(name='manager'):
            queryset = super().get_queryset()
        else:
            queryset = super().get_queryset().filter(owner=self.request.user)
        return queryset


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    template_name = 'mailing/client/client_form.html'
    form_client = ClientForm
    success_url = reverse_lazy('mailing:clients')
    fields = ('name', 'surname', 'email', 'is_active', 'comment')



    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Добавление пользователя'
        return context_data

    def form_valid(self, form):
        new_client = form.save()
        new_client.owner = self.request.user
        new_client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    template_name = 'mailing/client/client_form.html'
    form_client = ClientForm
    success_url = reverse_lazy('mailing:clients')
    fields = ('name', 'surname', 'email', 'is_active', 'comment')


    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Редактирование пользователя'
        return context_data

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'mailing/client/client_delete.html'
    success_url = reverse_lazy('mailing:clients')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Удаление пользователя'
        return context_data

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'mailing/client/client_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.object
        return context_data

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mailing/message/message_list.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = "Сообщения"
        return context_data

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.groups.filter(name='manager'):
            queryset = super().get_queryset()
        else:
            queryset = super().get_queryset().filter(owner=self.request.user)
        return queryset


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    template_name = 'mailing/message/message_form.html'
    form_class = MessageForm
    success_url = reverse_lazy('mailing:messages')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Создание сообщения'
        return context_data

    def form_valid(self, form):
        new_message = form.save()
        new_message.owner = self.request.user
        new_message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    template_name = 'mailing/message/message_form.html'
    form_class = MessageForm
    success_url = reverse_lazy('mailing:messages')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Редактирование "{self.object.title}"'
        return context_data

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'mailing/message/message_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.object
        return context_data


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'mailing/message/message_delete.html'
    success_url = reverse_lazy('mailing:messages')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Удаление сообщения'
        return context_data

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing/mailing_info/mailing_list.html'


    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Расписания'
        return context_data

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.groups.filter(name='manager'):
            queryset = super().get_queryset()
        else:
            queryset = super().get_queryset().filter(owner=self.request.user)
        return queryset


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_info/mailing_form.html'
    success_url = reverse_lazy('mailing:mailings')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Создание расписания'
        return context_data

    def form_valid(self, form):
        new_schedule = form.save()
        new_schedule.owner = self.request.user
        new_schedule.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_info/mailing_form.html'
    success_url = reverse_lazy('mailing:mailings')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Редактирование {self.object.message}'
        return context_data

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_info/mailing_delete.html'
    success_url = reverse_lazy('mailing:mailings')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Удаление'
        return context_data

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailing/mailing_info/mailing_detail.html'


    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.object.message

        schedule_item = Mailing.objects.get(pk=self.kwargs.get('pk'))
        user_item = Client.objects.filter(is_active=True)
        context_data['schedule_pk'] = schedule_item.pk
        context_data['user_item'] = user_item

        return context_data

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


@login_required
def toggle_active(request, pk):
    schedule = Mailing.objects.get(pk=pk)
    # Переключаем статус is_active, если только рассылка не завершена
    if schedule.status != 4:
        schedule.is_active = {schedule.is_active: False,
                              not schedule.is_active: True}[True]
        schedule.save()
    else:
        messages.error(request, 'You cannot deactivate completed schedule')
    return redirect(reverse('mailing:mailings'))


@login_required
def toggle_run_pause(request, pk):
    schedule = Mailing.objects.get(pk=pk)
    # Переключаем статус running/pause, если только рассылка не завершена
    if schedule.status != 4:
        schedule.status = {schedule.status == 5: 1,
                           schedule.status == 1 or schedule.status == 3: 5}[True]
        schedule.save()
    else:
        messages.error(request, 'You cannot run/pause completed schedule')
    return redirect(reverse('mailing:mailings'))


class MailingLogListView(LoginRequiredMixin, ListView):
    model = MailingLog
    template_name = 'mailing/mailinglog/mailinglog_list.html'


    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.schedule.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_superuser:
            queryset = super().get_queryset()
        else:
            queryset = super().get_queryset().filter(schedule__owner=self.request.user)
        return queryset


class MailingLogDetailView(LoginRequiredMixin, DetailView):
    model = MailingLog
    template_name = 'mailing/mailinglog/mailinglog_detail.html'


    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.schedule.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object
