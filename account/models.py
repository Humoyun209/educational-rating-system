from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 1
    USER = 2
    STUDY_SECTION = 3
    STATUS = (
        (ADMIN, 'admin'),
        (USER, 'foydalanuvchi'),
        (STUDY_SECTION, 'o\'quv bo\'limi')
    )
    position = models.SmallIntegerField(default=USER, choices=STATUS)