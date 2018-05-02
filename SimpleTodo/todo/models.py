from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

import uuid

class TodoItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    description = models.TextField()
