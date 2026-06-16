from reportlab.pdfgen import canvas

from .base import BaseConverter


class TextToPdfConverter(BaseConverter):

    source_formats = ["txt"]
    target_formats = ["pdf"]

    def convert(
        self,
        input_path,
        output_path
    ):
        pdf = canvas.Canvas(
            output_path
        )

        with open(
            input_path,
            "r",
            encoding="utf-8"
        ) as file:

            lines = file.readlines()

        y = 800

        for line in lines:
            pdf.drawString(
                50,
                y,
                line.strip()
            )

            y -= 20

        pdf.save()