from pathlib import Path
import argparse
import pandas as pd
import numpy as np


def read_table(file_path: Path, sheet_name: str | int | None = None) -> pd.DataFrame:
    suffix = file_path.suffix.lower()

    if suffix == ".csv":
        return pd.read_csv(file_path, dtype=str)

    if suffix in {".xlsx", ".xlsm", ".xltx", ".xltm", ".xls"}:
        return pd.read_excel(file_path, sheet_name=sheet_name, dtype=str)

    raise ValueError(f"Unsupported file type: {suffix}")


# 🔥 Strong normalization function
def normalize_code(x):
    if pd.isna(x):
        return np.nan
    return (
        str(x)
        .strip()
        .replace("\xa0", "")   # remove hidden non-breaking spaces
        .upper()
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Remove values existing in OUTLET CODE and shift remaining values up"
    )
    parser.add_argument("file", type=Path, help="Path to .csv/.xlsx file")
    parser.add_argument("--sheet", default=None,
                        help="Sheet name or index for Excel files")
    args = parser.parse_args()

    if not args.file.exists():
        raise FileNotFoundError(f"File not found: {args.file}")

    sheet = args.sheet
    if sheet is not None and sheet.isdigit():
        sheet = int(sheet)

    df = read_table(args.file, sheet_name=sheet)

    print("\n================ FILE INFO ================")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    df.columns = df.columns.str.strip()

    data_columns = [
        "SKIN_CARE_GAL_GOLD",
        "SKIN_CARE_PONDS_GOLD",
        "HAIR_CARE_GOLD_SLAB",
        "SKIN_CARE_GAL_DIAMOND",
        "SKIN_CARE_PONDS_DIAMOND",
        "HAIR_CARE_DIAMOND_SLAB"
    ]

    if "OUTLET CODE" not in df.columns:
        raise ValueError("Column 'OUTLET CODE' not found")

    # ✅ Normalize OUTLET CODE properly
    df["OUTLET CODE"] = df["OUTLET CODE"].apply(normalize_code)

    valid_outlets = set(df["OUTLET CODE"].dropna())

    print("\nMaster OUTLET CODE unique count:", len(valid_outlets))
    print("===========================================\n")

    print("========== PROCESSING COLUMNS ==========\n")

    for col in data_columns:
        if col not in df.columns:
            continue

        print(f"Processing: {col}")

        # Normalize column
        df[col] = df[col].apply(normalize_code)

        original_values = df[col].dropna()

        # Remove values existing in OUTLET CODE
        filtered_values = original_values[
            ~original_values.isin(valid_outlets)
        ].tolist()

        removed_count = len(original_values) - len(filtered_values)

        print(f"  Original values: {len(original_values)}")
        print(f"  Removed (matched OUTLET CODE): {removed_count}")
        print(f"  Remaining: {len(filtered_values)}")
        print("----------------------------------------")

        # ✅ Replace column directly (auto shift up)
        df[col] = pd.Series(filtered_values, dtype="object")

    print("\n✅ Processing Complete\n")

    output_file = args.file.parent / "Final Slabs V2.csv"
    df.to_csv(output_file, index=False)

    print(f"✅ New file saved as: {output_file}")


if __name__ == "__main__":
    main()
