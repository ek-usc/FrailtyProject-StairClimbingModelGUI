import numpy as np
import scipy.io as sio
import pandas as pd
import os
from pathlib import Path


def inspect_mat_file(filepath):
    print(f"\n--- Inspecting MAT file: {filepath.name} ---")
    try:
        mat = sio.loadmat(str(filepath))
        print(f"Keys found: {list(mat.keys())}")
        for key in mat:
            if not key.startswith('__'):
                val = mat[key]
                if isinstance(val, np.ndarray):
                    print(f"  Variable '{key}': Shape {val.shape}, Type {val.dtype}")
                    # Print a small slice to see content
                    if val.size > 0:
                        print(f"  Preview (first 2x2 or similar): \n{val.flat[:4]}")
                else:
                    print(f"  Variable '{key}': {type(val)}")
    except Exception as e:
        print(f"Error reading MAT file: {e}")


def inspect_sto_file(filepath):
    print(f"\n--- Inspecting STO/TXT file: {filepath.name} ---")
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
            print(f"Total lines: {len(lines)}")
            print("First 10 lines:")
            for i, line in enumerate(lines[:10]):
                print(f"  {i}: {line.strip()}")

            # Try parsing with pandas to see shape
            # Skip header logic for a quick check
            try:
                # Attempt to find end of header
                header_end = 0
                for i, line in enumerate(lines):
                    if 'endheader' in line:
                        header_end = i + 1
                        break

                if header_end > 0:
                    print(f"  Header ends at line {header_end}")
                    df = pd.read_csv(filepath, sep='\t', skiprows=header_end)
                    print(f"  Pandas parse (tab-sep) shape: {df.shape}")
                    print(f"  Columns: {list(df.columns[:5])} ...")
                else:
                    # Maybe space separated?
                    print("  No 'endheader' found. Trying basic load...")
                    data = np.loadtxt(filepath, skiprows=1)  # Assuming 1 header line if no endheader
                    print(f"  Numpy loadtxt shape: {data.shape}")
            except Exception as e:
                print(f"  Quick parse failed: {e}")

    except Exception as e:
        print(f"Error reading Text file: {e}")


def main():
    data_dir = Path("data")
    if not data_dir.exists():
        print(f"Error: Directory '{data_dir}' not found.")
        return

    files = list(data_dir.glob("*"))
    print(f"Found {len(files)} files in {data_dir}")

    for f in files:
        if f.suffix == '.mat':
            inspect_mat_file(f)
        elif f.suffix in ['.sto', '.txt']:
            inspect_sto_file(f)
        else:
            print(f"\nSkipping unknown file type: {f.name}")


if __name__ == "__main__":
    main()