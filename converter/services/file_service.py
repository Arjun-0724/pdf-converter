import os
import uuid
from django.conf import settings


def generate_unique_name(filename):
    extension = os.path.splitext(filename)[1]
    return f"{uuid.uuid4().hex}{extension}"


def get_upload_directory():
    upload_dir = os.path.join(
        settings.MEDIA_ROOT,
        "uploads"
    )

    os.makedirs(
        upload_dir,
        exist_ok=True
    )

    return upload_dir


def get_converted_directory():
    converted_dir = os.path.join(
        settings.MEDIA_ROOT,
        "converted"
    )

    os.makedirs(
        converted_dir,
        exist_ok=True
    )

    return converted_dir


def delete_file(path):
    try:
        if path and os.path.exists(path):
            os.remove(path)
    except Exception:
        pass