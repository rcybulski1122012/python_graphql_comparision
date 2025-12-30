import enum

import strawberry
import strawberry_django
from django.utils import timezone
from strawberry import auto, relay
from strawberry.relay import GlobalID

from python_graphql_comparison.tasks import models
from python_graphql_comparison.tasks.models import (
    Activity,
    CommentActivity,
    StatusChangeActivity,
    Task,
    User,
)


@strawberry_django.filter_type(User)
class UserFilter:
    id: GlobalID | None
    username: auto


@strawberry_django.type(User, name="User", filters=UserFilter)
class UserType(relay.Node):
    username: auto
    avatar_color: auto


@strawberry.enum(name="Priority")
class PriorityEnum(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


@strawberry.enum(name="Column")
class ColumnEnum(enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


@strawberry_django.filter_type(Task)
class TaskFilter:
    id: auto
    priority: PriorityEnum | None
    column: ColumnEnum | None
    description: auto
    assignee: UserFilter | None


@strawberry_django.order_type(Task)
class TaskOrder:
    priority: auto
    column: auto


@strawberry_django.type(models.Task, name="Task", filters=TaskFilter, ordering=TaskOrder)
class TaskType(relay.Node):
    title: auto
    priority: PriorityEnum
    column: ColumnEnum
    description: auto
    assignee: UserType | None
    created_at: auto
    updated_at: auto
    activities: list["ActivityInterface"]

    @strawberry_django.field(only=["created_at"])
    @staticmethod
    def days_open(task: strawberry.Parent[Task]) -> int:
        today = timezone.now().date()
        return (today - task.created_at.date()).days


@strawberry_django.interface(Activity, name="Activity")
class ActivityInterface(relay.Node):
    created_at: auto = strawberry_django.field(name="timestamp")
    actor: UserType


@strawberry_django.type(CommentActivity, name="CommentActivity")
class CommentActivityType(ActivityInterface):
    text: auto


@strawberry_django.type(StatusChangeActivity, name="StatusChangeActivity")
class StatusChangeActivityType(ActivityInterface):
    old_status: ColumnEnum
    new_status: ColumnEnum
