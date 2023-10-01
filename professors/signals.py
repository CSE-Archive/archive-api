import os
from pathlib import Path

from django.conf import settings
from django.db.models.signals import post_save

from core.helpers import receiver_with_dirty_transaction
from professors.models import Professor


@receiver_with_dirty_transaction(post_save, sender=Professor, dispatch_uid="set_professor_image_path")
def set_professor_image_path(sender, instance: Professor, **kwargs):
    if instance.image:
        image_extension = Path(instance.image.name).suffix
        image_name = instance.generate_unique_name() + image_extension
        image_path = os.path.join(instance.image.field.upload_to, image_name)
        os.rename(instance.image.path, os.path.join(settings.MEDIA_ROOT, image_path))
        instance.image.name = image_path
        instance.save()
