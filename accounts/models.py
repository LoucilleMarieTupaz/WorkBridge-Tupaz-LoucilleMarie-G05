from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrator"
        PROJECT_MANAGER = "PROJECT_MANAGER", "Project Manager"
        MEMBER = "MEMBER", "Project Member"

    role = models.CharField(
        max_length = 20,
        choices = Role.choices,
        default = Role.MEMBER
    )

    def __str__(self):
        return self.username