import json
import pyodbc
import pandas as pd
from pathlib import Path
from logger import log_info, log_error

# Hämtar sökväg till config
config_path = Path(__file__).parent.parent / "config" / "db_config.json"

# Läser in config-filen
try:
    with open(config_path, "r", encoding="utf-8") as file:
        config = json.load(file)
except Exception as e:
    log_error(f"Kunde inte läsa konfigurationsfilen: {e}")
    raise

# Hanterar Trusted_Connection som bool eller str
trusted = config.get("trusted_connection", True)
if isinstance(trusted, bool):
    trusted_value = "yes" if trusted else "no"
else:
    trusted_value = str(trusted)

# Bygger connection string för Windows Authentication
conn_str = (
    f"DRIVER={{{config['driver']}}};"
    f"SERVER={config['server']};"
    f"DATABASE={config['database']};"
    f"Trusted_Connection={trusted_value};"
)

# Testar anslutning och hämta sample-data
try:
    with pyodbc.connect(conn_str) as conn:
        log_info("Ansluten till databasen (extract.py)")

        query = """
        SELECT TOP 10
            soh.SalesOrderID,
            soh.OrderDate,
            soh.TotalDue,
            p.Name AS ProductName,
            sod.OrderQty AS QuantitySold,
            per.FirstName,
            per.LastName
        FROM Sales.SalesOrderHeader soh
        JOIN Sales.SalesOrderDetail sod 
            ON soh.SalesOrderID = sod.SalesOrderID
        JOIN Production.Product p 
            ON sod.ProductID = p.ProductID
        JOIN Sales.Customer c 
            ON soh.CustomerID = c.CustomerID
        LEFT JOIN Person.Person per 
            ON c.PersonID = per.BusinessEntityID
        ORDER BY soh.OrderDate DESC;
        """

        df = pd.read_sql(query, conn)
        log_info(f"Exempeldata hämtad: {df.shape[0]} rader")
        print(df.head())
except Exception as e:
    log_error(f"Kunde inte ansluta eller hämta data i extract.py: {e}")
    raise
