import pandas as pd
from pathlib import Path

def load_to_csv(df: pd.DataFrame, filename: str = "sales_data.csv") -> Path:
    """
    Sparar transformerad data som CSV i output-mappen och returnerar sökvägen.
    """
    output_path = Path(__file__).parent.parent / "output" / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Skriver CSV
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"Data sparad till {output_path}")
    return output_path
