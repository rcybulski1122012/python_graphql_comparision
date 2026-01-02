from ariadne import EnumType, InterfaceType
from ariadne.contrib.relay import RelayObjectType, encode_global_id
from asgiref.sync import sync_to_async
from django.utils import timezone

from python_graphql_comparison.tasks.models import (
    Activity,
    CommentActivity,
    StatusChangeActivity,
    Task,
    User,
)

task = RelayObjectType("Task")
user = RelayObjectType("User")
activity = InterfaceType("Activity")

task.set_field("id", lambda obj, *_: encode_global_id("Task", obj.id))
task.set_alias("status", "column")

user.set_field("id", lambda obj, *_: encode_global_id("User", obj.id))
activity.set_field("id", lambda obj, *_: encode_global_id("Activity", obj.id))


priority_enum = EnumType(
    "Priority",
    {
        "LOW": "low",
        "MEDIUM": "medium",
        "HIGH": "high",
        "URGENT": "urgent",
    },
)

column_enum = EnumType(
    "Column",
    {
        "TODO": "todo",
        "IN_PROGRESS": "in_progress",
        "REVIEW": "review",
        "DONE": "done",
    },
)


@task.field("daysOpen")
def resolve_days_open(obj: Task, *_) -> int:
    now = timezone.now()
    return (now - obj.created_at).days


@task.field("activities")
async def resolve_task_activities(obj: Task, *_) -> list[Activity]:
    # Should prefetch in tasks, or implement a dataloader
    return await sync_to_async(list)(obj.activities.all())


@activity.field("actor")
async def resolve_task_activity(obj: Task, *_) -> User:
    # Should prefetch in tasks, or implement a dataloader
    return await sync_to_async(getattr)(obj, "actor")


@activity.type_resolver
def resolve_activity_type(obj, *_) -> str:
    if isinstance(obj, CommentActivity):
        return "CommentActivity"
    if isinstance(obj, StatusChangeActivity):
        return "StatusChangeActivity"
    return None
