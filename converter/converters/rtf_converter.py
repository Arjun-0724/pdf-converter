import pypandoc
from .base import BaseConverter
import os
import tempfile
import pypandoc
import pythoncom
from docx2pdf import convert

from .base import BaseConverter

class RtfToDocxConverter(BaseConverter):
    source_formats = ["rtf"]
    target_formats = ["docx"]

    def convert(self, input_path, output_path):
        pypandoc.convert_file(
            input_path,
            "docx",
            outputfile=output_path
        )
        
import pypandoc
from .base import BaseConverter


class RtfToPdfConverter(BaseConverter):
    source_formats = ["rtf"]
    target_formats = ["pdf"]

    def convert(self, input_path, output_path):

        with tempfile.NamedTemporaryFile(
            suffix=".docx",
            delete=False
        ) as temp_file:

            temp_docx = temp_file.name

        try:
            pypandoc.convert_file(
                input_path,
                "docx",
                outputfile=temp_docx
            )

            pythoncom.CoInitialize()

            try:
                convert(
                    temp_docx,
                    output_path
                )
            finally:
                pythoncom.CoUninitialize()

        finally:
            if os.path.exists(temp_docx):
                os.remove(temp_docx)