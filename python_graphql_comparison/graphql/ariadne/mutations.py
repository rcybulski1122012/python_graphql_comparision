from typing import Any

from ariadne import MutationType
from ariadne.contrib.relay import decode_global_id

from python_graphql_comparison.tasks.models import Task

mutation = MutationType()


@mutation.field("createTask")
async def resolve_create_task(_, info, data: dict[str, Any]) -> Task:
    assignee_id = decode_global_id(data["assignee"]).id if "assignee" in data else None
    return await Task.objects.acreate(
        title=data["title"],
        priority=data["priority"],
        column=data["status"],
        description=data.get("description", ""),
        assignee_id=assignee_id,
    )


@mutation.field("updateTask")
async def resolve_update_task(_, info, **kwargs) -> Task:
    decoded_id = decode_global_id(kwargs["id"])
    task = await Task.objects.aget(id=decoded_id.id)
    data = kwargs["data"]

    if "title" in data and data["title"] is not None:
        task.title = data["title"]

    if "priority" in data and data["priority"] is not None:
        task.priority = data["priority"]

    if "status" in data and data["status"] is not None:
        task.status = data["status"]

    if "description" in data and data["description"] is not None:
        task.description = data["description"]

    if "assignee" in data and data["assignee"] is not None:
        task.assignee_id = decode_global_id(data["assignee"]).id

    await task.asave()
    return task


@mutation.field("deleteTask")
async def resolve_delete_task(_, info, **kwargs) -> Task:
    decoded_id = decode_global_id(kwargs["id"])
    task = await Task.objects.aget(id=decoded_id.id)
    await task.adelete()
    return task
