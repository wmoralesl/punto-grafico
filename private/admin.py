from django.contrib import admin

# Register your models here.
from .models import UserActionLog

@admin.register(UserActionLog)
class UserActionLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'model_name', 'object_id', 'timestamp', 'ip_address')
    search_fields = ('user__username', 'action', 'model_name', 'object_id')
    list_filter = ('timestamp', 'model_name')