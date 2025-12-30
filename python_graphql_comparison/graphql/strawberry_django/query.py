import strawberry
import strawberry_django
from strawberry.relay import Node
from strawberry_django.relay import DjangoListConnection

from python_graphql_comparison.graphql.strawberry_django.types import TaskType


@strawberry.type
class Query:
    node: Node | None = strawberry_django.node()
    task: TaskType | None = strawberry_django.node()
    tasks: DjangoListConnection[TaskType] = strawberry_django.connection()
