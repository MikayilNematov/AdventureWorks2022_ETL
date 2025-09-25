import pandas as pd

def transform_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Tar rå försäljningsdata och gör den renare för analys i Power BI.
    Klarar både om CustomerName redan finns eller om man har FirstName/LastName.
    """
    if df is None:
        raise ValueError("Argumentet df får inte vara None")

    df = df.copy()

    # Skapar CustomerName endast om den saknas
    if "CustomerName" not in df.columns:
        if "FirstName" in df.columns and "LastName" in df.columns:
            df["CustomerName"] = (
                df["FirstName"].fillna("").astype(str).str.strip()
                + " "
                + df["LastName"].fillna("").astype(str).str.strip()
            ).str.strip()
        elif "Store" in df.columns:
            df["CustomerName"] = df["Store"].astype(str)
        elif "CustomerID" in df.columns:
            df["CustomerName"] = df["CustomerID"].astype(str)
        else:
            df["CustomerName"] = "Okänd kund"

    # Behåller bara relevanta kolumner (de som faktiskt finns)
    desired_cols = [
        "SalesOrderID",
        "OrderDate",
        "ProductName",
        "CustomerName",
        "OrderQty",
        "QuantitySold",
        "TotalDue",
        "Country",
        "Region",
        "City"
    ]
    cols_to_keep = [c for c in desired_cols if c in df.columns]
    df_clean = df[cols_to_keep].copy()

    # Konverterar datatyper
    if "OrderDate" in df_clean.columns:
        df_clean["OrderDate"] = pd.to_datetime(df_clean["OrderDate"], errors="coerce")

    if "TotalDue" in df_clean.columns:
        df_clean["TotalDue"] = pd.to_numeric(df_clean["TotalDue"], errors="coerce")

    if "OrderQty" in df_clean.columns:
        df_clean["OrderQty"] = pd.to_numeric(df_clean["OrderQty"], errors="coerce")
    elif "QuantitySold" in df_clean.columns:
        df_clean["OrderQty"] = pd.to_numeric(df_clean["QuantitySold"], errors="coerce")
        df_clean.drop(columns=["QuantitySold"], inplace=True, errors="ignore")

    return df_clean.reset_index(drop=True)
