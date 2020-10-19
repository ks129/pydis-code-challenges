from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Extended user model for our use."""

    verified = models.BooleanField(
        "Verified by staff", default=False, help_text="Is user able to participate on event?"
    )
