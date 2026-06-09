import os
from reportlab.graphics.barcode import createBarcodeDrawing


class BarcodeUtils:

    @staticmethod
    def generate_barcode(
        barcode_value: str
    ):

        os.makedirs(
            "uploads/barcodes",
            exist_ok=True
        )

        barcode = createBarcodeDrawing(
            "Code128",
            value=barcode_value,
            humanReadable=True
        )

        file_path = (
            f"uploads/barcodes/"
            f"{barcode_value}.svg"
        )

        svg_data = barcode.asString("svg")

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:
            file.write(svg_data)

        print(
            "FILE EXISTS:",
            os.path.exists(file_path),
            flush=True
        )

        print(
            "FILE PATH:",
            os.path.abspath(file_path),
            flush=True
        )

        return (
            f"/uploads/barcodes/"
            f"{barcode_value}.svg"
        )