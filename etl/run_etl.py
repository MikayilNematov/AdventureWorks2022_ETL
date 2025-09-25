import pyodbc
import pandas as pd
import json
from pathlib import Path
from transform import transform_sales_data
from load import load_to_csv
from logger import log_info, log_error

# Hämtar config
config_path = Path(__file__).parent.parent / "config" / "db_config.json"
with open(config_path, "r", encoding="utf-8") as file:
    config = json.load(file)

# Hanterar Trusted_Connection som bool eller str
trusted = config.get("trusted_connection", True)
if isinstance(trusted, bool):
    trusted_value = "yes" if trusted else "no"
else:
    trusted_value = str(trusted)

# Bygger connection string
conn_str = (
    f"DRIVER={{{config['driver']}}};"
    f"SERVER={config['server']};"
    f"DATABASE={config['database']};"
    f"Trusted_Connection={trusted_value};"
)

def run_etl():
    try:
        log_info("ETL-process startad")

        # Extract
        with pyodbc.connect(conn_str) as conn:
            log_info("Ansluten till databasen")

            query = """
                SELECT
                    soh.SalesOrderID,
                    soh.OrderDate,
                    p.Name AS ProductName,
                    CASE 
                        WHEN per.BusinessEntityID IS NOT NULL 
                            THEN per.FirstName + ' ' + per.LastName
                        ELSE st.Name
                    END AS CustomerName,
                    sod.OrderQty,
                    soh.TotalDue,
                    cr.Name AS Country,
                    sp.Name AS Region,
                    a.City
                FROM Sales.SalesOrderHeader soh
                JOIN Sales.SalesOrderDetail sod 
                    ON soh.SalesOrderID = sod.SalesOrderID
                JOIN Production.Product p 
                    ON sod.ProductID = p.ProductID
                JOIN Sales.Customer c 
                    ON soh.CustomerID = c.CustomerID
                LEFT JOIN Person.Person per 
                    ON c.PersonID = per.BusinessEntityID
                LEFT JOIN Sales.Store st 
                    ON c.StoreID = st.BusinessEntityID
                JOIN Person.Address a 
                    ON soh.BillToAddressID = a.AddressID
                JOIN Person.StateProvince sp 
                    ON a.StateProvinceID = sp.StateProvinceID
                JOIN Person.CountryRegion cr 
                    ON sp.CountryRegionCode = cr.CountryRegionCode
                ORDER BY soh.OrderDate;
            """

            df_raw = pd.read_sql(query, conn)

        log_info(f"Data extraherad: {df_raw.shape[0]} rader")
        log_info(f"Kolumner: {df_raw.columns.tolist()}")

        # Transform
        df_clean = transform_sales_data(df_raw)
        log_info(f"Data transformerad: {df_clean.shape[0]} rader")

        # Load
        out_path = load_to_csv(df_clean)
        log_info(f"Data laddad till CSV: {out_path}")

        log_info("ETL-process klar")

    except Exception as e:
        log_error(f"Fel under ETL-processen: {e}")
        # Re-raise så att stacktrace syns i konsolen om du kör manuellt
        raise

if __name__ == "__main__":
    run_etl()
