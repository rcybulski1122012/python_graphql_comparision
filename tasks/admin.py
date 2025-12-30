from django.contrib import admin
from .models import Task, CommentActivity, StatusChangeActivity

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'column', 'assignee', 'created_at', 'updated_at')
    list_filter = ('priority', 'column', 'assignee')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'


@admin.register(CommentActivity)
class CommentActivityAdmin(admin.ModelAdmin):
    list_display = ('actor', 'text', 'created_at')
    list_filter = ('actor', 'created_at')
    search_fields = ('text',)


@admin.register(StatusChangeActivity)
class StatusChangeActivityAdmin(admin.ModelAdmin):
    list_display = ('actor', 'old_status', 'new_status', 'created_at')
    list_filter = ('actor', 'old_status', 'new_status', 'created_at')
