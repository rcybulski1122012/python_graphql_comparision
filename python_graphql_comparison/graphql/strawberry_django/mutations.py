import strawberry
import strawberry_django
from strawberry import auto
from strawberry_django import NodeInput

from python_graphql_comparison.graphql.strawberry_django.types import (
    ColumnEnum,
    PriorityEnum,
    TaskType,
)
from python_graphql_comparison.tasks.models import Task


@strawberry_django.input(Task)
class CreateTaskInput:
    title: auto
    priority: PriorityEnum
    status: ColumnEnum
    description: auto
    assignee: auto


@strawberry_django.partial(Task)
class UpdateTaskInput(NodeInput):
    title: auto
    priority: PriorityEnum | None
    status: ColumnEnum | None
    description: auto
    assignee: auto


@strawberry.type
class Mutation:
    create_task: TaskType = strawberry_django.mutations.create(
        CreateTaskInput, handle_django_errors=True
    )
    update_task: TaskType = strawberry_django.mutations.update(
        UpdateTaskInput, handle_django_errors=True
    )
    delete_task: TaskType = strawberry_django.mutations.delete(NodeInput, handle_django_errors=True)
