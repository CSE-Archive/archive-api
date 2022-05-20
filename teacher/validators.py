from django.core.exceptions import ValidationError


def image_size_validator(image):
    max_size = 1

    if int(image.size) > max_size * 1024 * 1024:
        raise ValidationError(f"حجم عکس‌ها نمی‌تواند بیشتر از {max_size} مگابایت باشد.")
