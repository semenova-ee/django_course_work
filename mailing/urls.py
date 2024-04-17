from django.urls import path

from mailing.apps import DjangoCourseWorkConfig
from mailing.views import IndexView, ClientDetailView, ClientCreateView, ClientDeleteView, ClientUpdateView, \
    ClientListView, MessageCreateView, MessageListView, MessageUpdateView, MessageDeleteView, MessageDetailView, \
    MailingListView, \
    MailingCreateView, MailingUpdateView, MailingDeleteView, MailingDetailView, toggle_active, \
    MailingLogListView, MailingLogDetailView

app_name = DjangoCourseWorkConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('clients/', ClientListView.as_view(), name='clients'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('clients/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('clients/detail/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),

    path('messages/', MessageListView.as_view(), name='messages'),
    path('messages/create', MessageCreateView.as_view(), name='message_create'),
    path('messages/update/<int:pk>', MessageUpdateView.as_view(), name='message_update'),
    path('messages/detail/<int:pk>', MessageDetailView.as_view(), name='message_detail'),
    path('messages/delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),

    path('mailings/', MailingListView.as_view(), name='mailings'),
    path('mailings/create', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/update/<int:pk>', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailings/delete/<int:pk>', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailings/detail/<int:pk>', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailings/toggle_active/<int:pk>', toggle_active, name='toggle_active'),
    # path('mailings/toggle_run_pause/<int:pk>', toggle_run_pause, name='toggle_run_pause'),

    path('mailing_logs/', MailingLogListView.as_view(), name='mailing_logs'),
    path('mailing_logs/view/<int:pk>', MailingLogDetailView.as_view(), name='mailinglog_view'),
]