from django.contrib import admin

from members.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone',)
    list_filter = ('id',)