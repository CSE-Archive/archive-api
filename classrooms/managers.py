from django.db import models

from core.models import BaseManager


class TaManager(models.Manager):
    def get_by_natural_key(self, uuid: str):
        return self.get(uuid=uuid)


class ClassroomManager(BaseManager):
    ...
