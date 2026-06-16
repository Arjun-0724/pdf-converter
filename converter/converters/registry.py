from .docx_converter import (
    DocxToPdfConverter
)

from .text_converter import (
    TextToPdfConverter
)
from .image_converter import (
    JpgToPngConverter,
    PngToJpgConverter,
)

CONVERTERS = [
    DocxToPdfConverter(),
    TextToPdfConverter(),
    JpgToPngConverter(),
    PngToJpgConverter(),
]


def get_converter(
    source_format,
    target_format
):

    for converter in CONVERTERS:

        if (
            source_format
            in converter.source_formats
            and
            target_format
            in converter.target_formats
        ):
            return converter

    return None

def get_target_formats(
    source_format
):
    formats = []

    for converter in CONVERTERS:
        if (
            source_format
            in converter.source_formats
        ):
            formats.extend(
                converter.target_formats
            )

    return sorted(
        list(set(formats))
    )