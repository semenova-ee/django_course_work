from django.contrib import admin
# from django.db.models import Q

from mailing.models import Client, Message, MailingLog, Mailing


@admin.register(Client)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_active', 'created_at')
    list_filter = ('created_at',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'text')
    list_filter = ('created_at',)

    # def get_search_results(self, request, queryset, search_term):
    #     search_term_list = search_term.split(' ')
    #
    #     if not any(search_term_list):
    #         return queryset, False
    #
    #     name_query = Q(name__icontains=search_term)
    #     description_query = Q(description__icontains=search_term)
    #     queryset = queryset.filter(name_query | description_query)
    #
    #     return queryset, False


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'interval', 'status')
    list_filter = ('start_date',)


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('time', 'status', 'server_response', 'schedule')
    list_filter = ('time',)
