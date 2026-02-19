# Excel / CSV Reader (uv)

Simple `uv` project to read CSV and Excel files using `pandas`.

## Setup

```powershell
uv sync
```

## Run

Read a CSV file:

```powershell
uv run main.py "store\slab_update_final_removed_outlets_19th Feb.csv"
```

Read an Excel file:

```powershell
uv run main.py "report.xlsx" --sheet Sheet1 --rows 20
```

Notes:

- `--sheet` is only used for Excel files.
- `--sheet` accepts either a sheet name (`Sheet1`) or index (`0`).
