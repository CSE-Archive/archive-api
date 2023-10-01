import os
from pathlib import Path

from django.conf import settings
from django.db.models.signals import post_save

from core.helpers import receiver_with_dirty_transaction
from references.models import Reference


@receiver_with_dirty_transaction(post_save, sender=Reference, dispatch_uid="set_reference_file_path")
def set_reference_file_path(sender, instance: Reference, **kwargs):
    if instance.file:
        file_extension = Path(instance.file.name).suffix
        file_name = instance.generate_unique_name() + file_extension
        file_path = os.path.join(instance.file.field.upload_to, file_name)
        os.rename(instance.file.path, os.path.join(settings.MEDIA_ROOT, file_path))
        instance.file.name = file_path
        instance.save()


@receiver_with_dirty_transaction(post_save, sender=Reference, dispatch_uid="set_reference_cover_image_path")
def set_reference_cover_image_path(sender, instance: Reference, **kwargs):
    if instance.cover_image:
        image_extension = Path(instance.cover_image.name).suffix
        image_name = instance.generate_unique_name() + image_extension
        image_path = os.path.join(instance.cover_image.field.upload_to, image_name)
        os.rename(instance.cover_image.path, os.path.join(settings.MEDIA_ROOT, image_path))
        instance.cover_image.name = image_path
        instance.save()
