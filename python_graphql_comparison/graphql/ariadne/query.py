from ariadne.contrib.relay import (
    ConnectionArguments,
    RelayConnection,
    RelayQueryType,
    decode_global_id,
)

from python_graphql_comparison.tasks.models import Task

from .connection import ObjectConnection
from .utils import decode_cursor

query = RelayQueryType()


@query.field("task")
async def resolve_task(*_, **kwargs) -> Task | None:
    decoded_id = decode_global_id(kwargs["id"])
    return await Task.objects.filter(pk=decoded_id.id).afirst()


@query.connection("tasks")
async def resolve_tasks(
    _, _info, connection_arguments: ConnectionArguments, **kwargs
) -> RelayConnection | None:
    qs = Task.objects.all()

    if connection_arguments.last:
        qs = qs.order_by("-id")

        if connection_arguments.before:
            cursor = decode_cursor(connection_arguments.before)
            if cursor:
                qs = qs.filter(id__lt=cursor)

        limit = connection_arguments.last
        nodes = [n async for n in qs[: limit + 1]]

        has_previous_page = len(nodes) > limit
        if has_previous_page:
            nodes = nodes[:-1]

        nodes.reverse()
        has_next_page = False

    else:
        qs = qs.order_by("id")

        if connection_arguments.after:
            cursor = decode_cursor(connection_arguments.after)
            if cursor:
                qs = qs.filter(id__gt=cursor)

        limit = connection_arguments.first or 10
        nodes = [n async for n in qs[: limit + 1]]

        has_next_page = len(nodes) > limit
        if has_next_page:
            nodes = nodes[:-1]

        has_previous_page = False

    return ObjectConnection(
        edges=nodes,
        total=await qs.acount(),
        has_next_page=has_next_page,
        has_previous_page=has_previous_page,
    )
