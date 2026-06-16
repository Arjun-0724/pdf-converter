import pandas as pd
from .base import BaseConverter

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle
)
from reportlab.lib import colors

class CsvToXlsxConverter(BaseConverter):
    source_formats = ["csv"]
    target_formats = ["xlsx"]

    def convert(self, input_path, output_path):
        df = pd.read_csv(input_path)
        df.to_excel(
            output_path,
            index=False
        )



class XlsxToCsvConverter(BaseConverter):
    source_formats = ["xlsx"]
    target_formats = ["csv"]

    def convert(self, input_path, output_path):
        df = pd.read_excel(input_path)
        df.to_csv(
            output_path,
            index=False
        )
        
class XlsxToPdfConverter(BaseConverter):
    source_formats = ["xlsx"]
    target_formats = ["pdf"]

    def convert(self, input_path, output_path):
        df = pd.read_excel(input_path)

        data = [df.columns.tolist()]
        data.extend(
            df.values.tolist()
        )

        pdf = SimpleDocTemplate(
            output_path
        )

        table = Table(data)

        table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey,
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        1,
                        colors.black,
                    ),
                ]
            )
        )

        pdf.build([table])