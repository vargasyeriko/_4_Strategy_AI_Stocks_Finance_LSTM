Default panel file: your_data.pkl

Format (recommended): portable dict pickle `fmt: b3_panel_v1` — numpy values + ISO date strings + MultiIndex columns. Loads with pandas + numpy only (no PyArrow).

Legacy: a standard pandas DataFrame pickle may work if it was saved without Arrow-backed types; otherwise install PyArrow (`pip install pyarrow`).

Backup of the older Arrow-dependent file (if present): your_data.pkl.bak_pyarrow
