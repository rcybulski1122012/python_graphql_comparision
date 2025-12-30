from django.contrib.auth.models import AbstractUser
from django.db import models
from utils.fields import HexColorField


class User(AbstractUser):
    avatar_color = HexColorField(
        blank=True,
        null=True,
        help_text='Hex color code for user avatar (e.g., #FF5733)',
    )
