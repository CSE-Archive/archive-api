import os

from django.conf import settings
from django.db.models.signals import post_save

from core.helpers import receiver_with_dirty_transaction
from references.models import Reference


@receiver_with_dirty_transaction(post_save, sender=Reference, dispatch_uid="set_reference_file_path")
def set_file_path(sender, instance: Reference, **kwargs):
    if instance.file:
        file_name = instance.generate_file_name()
        file_path = os.path.join(instance.file.field.upload_to, file_name)
        os.rename(instance.file.path, os.path.join(settings.MEDIA_ROOT, file_path))
        instance.file.name = file_path
        instance.save()
