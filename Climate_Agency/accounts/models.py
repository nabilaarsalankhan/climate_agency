from django.contrib.auth.models import AbstractUser
import models
from django.db import models
import views




class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.username
        pass