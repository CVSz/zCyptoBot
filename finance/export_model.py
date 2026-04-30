from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font


OUTPUT_FILE = Path(__file__).resolve().parents[1] / "zeaz_financial_model.xlsx"


def build_model(years: int = 5) -> Workbook:
    wb = Workbook()
    ws = wb.active
    ws.title = "Financial Model"

    headers = ["Year", "ARR", "Growth", "Profit", "Burn"]
    ws.append(headers)

    for cell in ws[1]:
        cell.font = Font(bold=True)

    arr = 1_000_000
    growth = 0.2
    margin = 0.7
    burn = 500_000

    for year in range(1, years + 1):
        arr = arr * (1 + growth)
        profit = arr * margin
        ws.append([year, arr, growth, profit, burn])

    ws.freeze_panes = "A2"
    return wb


def export_model(output_file: Path = OUTPUT_FILE) -> Path:
    workbook = build_model()
    workbook.save(output_file)
    return output_file


if __name__ == "__main__":
    path = export_model()
    print(f"saved: {path}")
