from pdf2docx import Converter
from .base import BaseConverter


class PdfToDocxConverter(BaseConverter):
    source_formats = ["pdf"]
    target_formats = ["docx"]

    def convert(self, input_path, output_path):
        cv = Converter(input_path)
        cv.convert(output_path)
        cv.close()
        
import fitz
# from striprtf.striprtf import rtf_escape
from .base import BaseConverter


# class PdfToRtfConverter(BaseConverter):
    # source_formats = ["pdf"]
    # target_formats = ["rtf"]

    # def convert(self, input_path, output_path):
    #     doc = fitz.open(input_path)

    #     text = ""

    #     for page in doc:
    #         text += page.get_text()

    #     rtf = (
    #         "{\\rtf1\\ansi\n"
    #         + rtf_escape(text)
    #         + "\n}"
    #     )

    #     with open(
    #         output_path,
    #         "w",
    #         encoding="utf-8"
    #     ) as file:
    #         file.write(rtf)