from django.contrib import admin
from .models import Conversion


@admin.register(Conversion)
class ConversionAdmin(admin.ModelAdmin):

    list_display = (
        "original_name",
        "source_format",
        "target_format",
        "status",
        "created_at",
    )

    list_filter = (
        "source_format",
        "target_format",
        "status",
    )

    search_fields = (
        "original_name",
        "stored_name",
    )