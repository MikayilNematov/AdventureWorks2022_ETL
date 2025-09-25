# 🛠️ ETL-pipeline för AdventureWorks

Detta projekt är en enkel ETL-pipeline byggd i **Python** för att extrahera, transformera och ladda försäljningsdata från **SQL Server AdventureWorks2022**-databasen.  
Syftet är att förbereda datan för analys i t.ex. **Power BI** eller andra BI-verktyg.

---

## 📂 Projektstruktur

```
project-root/
├── config/
│   ├── db_config.example.json   # Exempel på databas-konfiguration
│   └── db_config.json           # Lokal kopia (gitignored)
│
├── etl/
│   ├── run_etl.py               # Orkestrerar hela ETL-processen
│   ├── extract.py               # Extraktion av data
│   ├── transform.py             # Rensar och förbereder data
│   ├── load.py                  # Laddar resultat till CSV
│   └── logger.py                # Hanterar loggning
│
├── output/                      # Resultatfiler (CSV)
├── logs/                        # Loggfiler
├── reports/                     # Power BI-rapporter (.pbix)
└── README.md
```

---

## 🗄️ Databasinställning

Filen `config/db_config.json` styr anslutningen mot din SQL Server.  
Den ingår inte i Git av säkerhetsskäl.  

Använd `config/db_config.example.json` som mall och skapa din egen lokala `db_config.json`.

Exempel på `db_config.example.json`:

```json
{
  "driver": "ODBC Driver 17 for SQL Server",
  "server": "localhost\\SQLEXPRESS",
  "database": "AdventureWorks2022",
  "trusted_connection": true
}
```

👉 Byt ut `server` mot din instans och sätt `trusted_connection` till `false` om du vill använda användarnamn/lösenord.

---

## ▶️ Körning

Starta ETL-processen med:

```bash
python etl/run_etl.py
```

Processen gör då:

1. **Extract** – hämtar försäljningsdata från AdventureWorks2022  
2. **Transform** – standardiserar kundnamn, konverterar datatyper och rensar kolumner  
3. **Load** – sparar resultatet som CSV i `output/sales_data.csv`

---

## 📊 Resultat

- Output: `output/sales_data.csv` (redo att importeras i Power BI eller andra verktyg)  
- Loggar: `logs/etl_log.txt` och `logs/etl_error_log.txt`

---

## 📈 Power BI-rapport

Detta repo innehåller även en Power BI-rapport baserad på försäljningsdatan från ETL-flödet.  
Rapporten visar bland annat:

- Försäljning per land, region och stad  
- Toppsäljande produkter  
- Total försäljning över tid  
- Kundsegmentering (personer vs butiker)  

---

## 🔗 Användning

1. Kör ETL-processen för att generera en färsk `sales_data.csv` i `output/`  
2. Öppna Power BI Desktop och ladda in `sales_data.csv`  
3. Uppdatera rapporten med senaste data 
