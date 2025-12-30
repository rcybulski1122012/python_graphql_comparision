import random
from typing import Any

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from python_graphql_comparison.tasks.models import (
    Column,
    CommentActivity,
    Priority,
    StatusChangeActivity,
    Task,
)

User = get_user_model()


class Command(BaseCommand):
    help = "Populates the database with dummy data"

    def handle(self, **_kwargs: Any) -> None:
        self.stdout.write("Creating dummy data...")

        # Create 5 users
        users = self._create_users()

        # Create 20 tasks
        tasks = self._create_tasks(users)

        # Create 0-3 activities per task
        self._create_activities(tasks, users)

        self.stdout.write(self.style.SUCCESS("Successfully created dummy data!"))
        self.stdout.write(f"Created {len(users)} users")
        self.stdout.write(f"Created {len(tasks)} tasks")

    def _create_users(self) -> list[User]:
        users = []
        for i in range(1, 6):
            username = f"user{i}"

            # Skip if user already exists
            if User.objects.filter(username=username).exists():
                users.append(User.objects.get(username=username))
                continue

            user = User.objects.create_user(
                username=username,
                email=f"{username}@example.com",
                password="password",
                first_name=f"First{i}",
                last_name=f"Last{i}",
                avatar_color=f"#{random.randint(0, 0xFFFFFF):06x}",
            )
            users.append(user)

        return users

    def _create_tasks(self, users: list[User]) -> list[Task]:
        tasks = []
        for i in range(1, 21):
            title = f"Task {i}"

            # Skip if task already exists
            if Task.objects.filter(title=title).exists():
                tasks.append(Task.objects.get(title=title))
                continue

            task = Task.objects.create(
                title=title,
                priority=random.choice(Priority.choices)[0],
                column=random.choice(Column.choices)[0],
                description=f"This is the description for task {i}",
                assignee=random.choice(users),
            )
            tasks.append(task)

        return tasks

    def _create_activities(self, tasks: list[Task], users: list[User]) -> None:
        activity_count = 0

        for task in tasks:
            # Create 0-3 activities per task
            num_activities = random.randint(0, 3)

            for _ in range(num_activities):
                # Randomly choose between CommentActivity and StatusChangeActivity
                activity_type = random.choice(["comment", "status"])
                actor = random.choice(users)

                if activity_type == "comment":
                    # Create a CommentActivity
                    CommentActivity.objects.create(
                        actor=actor, task=task, text=f"This is a comment on task {task.title}"
                    )
                else:
                    # Create a StatusChangeActivity
                    old_status = random.choice(Column.choices)[0]
                    # Ensure new_status is different from old_status
                    new_status_choices = [s[0] for s in Column.choices if s[0] != old_status]
                    new_status = random.choice(new_status_choices)

                    StatusChangeActivity.objects.create(
                        actor=actor, task=task, old_status=old_status, new_status=new_status
                    )

                activity_count += 1

        self.stdout.write(f"Created {activity_count} activities")
