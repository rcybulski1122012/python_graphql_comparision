from pathlib import Path

from ariadne import load_schema_from_path, make_executable_schema

from python_graphql_comparison.graphql.ariadne.mutations import mutation
from python_graphql_comparison.graphql.ariadne.query import query
from python_graphql_comparison.graphql.ariadne.types import (
    activity,
    column_enum,
    priority_enum,
    task,
    user,
)

type_defs = load_schema_from_path(Path(__file__).parent.parent.parent.parent / "schema.graphql")

schema = make_executable_schema(
    type_defs, query, task, activity, user, mutation, column_enum, priority_enum
)
