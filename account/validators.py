from django.core.exceptions import ValidationError
import os


def allow_only_images_validator(value):
    extension = os.path.splitext(value.name)[1]
    valid_extensions = ['.png', '.jpg', '.apng', '.avif', '.webp']
    if extension.lower() not in valid_extensions:
        raise ValidationError(f'Unsupported file \'{value}\'. Allowed file extensions: {", ".join(map(str, valid_extensions))}')
