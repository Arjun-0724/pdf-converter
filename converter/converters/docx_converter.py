from docx2pdf import convert
import pythoncom

from .base import BaseConverter


class DocxToPdfConverter(BaseConverter):

    source_formats = ["docx"]
    target_formats = ["pdf"]

    def convert(
        self,
        input_path,
        output_path
    ):
        pythoncom.CoInitialize()

        try:
            convert(
                input_path,
                output_path
            )
        finally:
            pythoncom.CoUninitialize()