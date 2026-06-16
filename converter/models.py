from django.db import models


class Conversion(models.Model):
    original_name = models.CharField(
        max_length=255
    )

    stored_name = models.CharField(
        max_length=255
    )

    source_format = models.CharField(
        max_length=20
    )

    target_format = models.CharField(
        max_length=20
    )

    status = models.CharField(
        max_length=20,
        default="Success"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.original_name}"
            f" → "
            f"{self.target_format}"
        )