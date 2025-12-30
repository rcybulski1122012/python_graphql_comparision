from django.contrib.auth.models import AbstractUser

from python_graphql_comparison.utils.fields import HexColorField


class User(AbstractUser):
    avatar_color = HexColorField(
        blank=True,
        null=True,
        help_text="Hex color code for user avatar (e.g., #FF5733)",
    )
