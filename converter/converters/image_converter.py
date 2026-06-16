from PIL import Image
from .base import BaseConverter


class JpgToPngConverter(BaseConverter):

    source_formats = ["jpg", "jpeg"]
    target_formats = ["png"]

    def convert(
        self,
        input_path,
        output_path
    ):
        image = Image.open(
            input_path
        )

        image.save(
            output_path,
            "PNG"
        )


class PngToJpgConverter(BaseConverter):

    source_formats = ["png"]
    target_formats = ["jpg"]

    def convert(
        self,
        input_path,
        output_path
    ):
        image = Image.open(
            input_path
        )

        image = image.convert(
            "RGB"
        )

        image.save(
            output_path,
            "JPEG"
        )