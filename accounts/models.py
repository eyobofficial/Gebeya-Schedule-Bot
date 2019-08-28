from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)

    def __str__(self):
        return self.username
