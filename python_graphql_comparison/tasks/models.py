from django.contrib.auth import get_user_model
from django.db import models
from polymorphic.models import PolymorphicModel

User = get_user_model()


class Priority(models.TextChoices):
    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"
    URGENT = "urgent", "Urgent"


class Column(models.TextChoices):
    TODO = "todo", "Todo"
    IN_PROGRESS = "in_progress", "In Progress"
    DONE = "done", "Done"


class Task(models.Model):
    title = models.CharField(max_length=100, blank=True, default="")
    priority = models.CharField(choices=Priority.choices, max_length=20)
    column = models.CharField(choices=Column.choices, max_length=20)
    description = models.TextField(blank=True, default="", max_length=1000)
    assignee = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Activity(PolymorphicModel):
    actor = models.ForeignKey(User, on_delete=models.PROTECT)
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="activities", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)


class CommentActivity(Activity):
    text = models.TextField(blank=True, default="", max_length=1000)

    class Meta:
        verbose_name_plural = "Comment activities"


class StatusChangeActivity(Activity):
    old_status = models.CharField(choices=Column.choices, max_length=20)
    new_status = models.CharField(choices=Column.choices, max_length=20)

    class Meta:
        verbose_name_plural = "Status change activities"
