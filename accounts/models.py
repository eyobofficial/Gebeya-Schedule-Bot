from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    telegram_id = models.CharField(max_length=30, unique=True, editable=False)
    is_manually_added = models.BooleanField(default=False)
