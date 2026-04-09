from io import BytesIO, StringIO
from typing import Any

import pandas as pd


def build_dataframe(records: list[dict[str, Any]]) -> pd.DataFrame:
    return pd.DataFrame(records)


def export_dataframe(frame: pd.DataFrame, filename_base: str, export_format: str) -> tuple[bytes, str, str]:
    if export_format == "excel":
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            frame.to_excel(writer, index=False, sheet_name="data")
        return (
            buffer.getvalue(),
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            f"{filename_base}.xlsx",
        )

    csv_buffer = StringIO()
    frame.to_csv(csv_buffer, index=False)
    return (
        csv_buffer.getvalue().encode("utf-8"),
        "text/csv; charset=utf-8",
        f"{filename_base}.csv",
    )
