from strawberry import Schema
from strawberry_django.optimizer import DjangoOptimizerExtension

from python_graphql_comparison.graphql.strawberry_django.mutations import Mutation
from python_graphql_comparison.graphql.strawberry_django.query import Query
from python_graphql_comparison.graphql.strawberry_django.scalars import ColorCode
from python_graphql_comparison.graphql.strawberry_django.types import (
    CommentActivityType,
    StatusChangeActivityType,
)

schema = Schema(
    query=Query,
    mutation=Mutation,
    extensions=[DjangoOptimizerExtension()],
    types=[CommentActivityType, StatusChangeActivityType, ColorCode],
)
