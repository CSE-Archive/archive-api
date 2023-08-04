from django.db import models

from core.models import BaseManager


class AuthorManager(models.Manager):
    def get_by_natural_key(self, full_name: str):
        return self.get(full_name=full_name)


class ReferenceManager(BaseManager):
    ...
