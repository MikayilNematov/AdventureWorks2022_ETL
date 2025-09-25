📄 README.md
# 🛠️ ETL-pipeline för AdventureWorks

Detta projekt är en enkel ETL-pipeline byggd i **Python** för att extrahera, transformera och ladda försäljningsdata från **SQL Server AdventureWorks2022**-databasen.  
Syftet är att förbereda datan för analys i t.ex. **Power BI** eller andra BI-verktyg.

---

## 📂 Projektstruktur

project-root/
│
├── config/
│   ├── db_config.example.json # Exempel på databas-konfiguration
│   └── db_config.json         # **Ej inkluderad i repo (gitignored)**, använd som lokal kopia
│
├── etl/
│   ├── run_etl.py.py                # Orkestrerar hela ETL-processen
│   ├── extract.py             # (exempel på extraktlogik)
│   ├── transform.py           # Rensar och förbereder data
│   ├── load.py                # Sparar resultatet till CSV
│   └── logger.py              # Hanterar loggning
│
├── output/                    # Här sparas resultatfiler (CSV)
│
├── logs/                      # Här sparas loggfiler
│
├── reports/                   # Power BI-rapporter (.pbix)
│
└── README.md

---

🗄️ Databasinställning

Filen config/db_config.json styr anslutningen mot din SQL Server. Den ingår inte i Git av säkerhetsskäl.
Du kan använda config/db_config.example.json som mall och skapa din egen lokala db_config.json.

Exempel på db_config.example.json:

{
  "driver": "ODBC Driver 17 for SQL Server",
  "server": "localhost\\SQLEXPRESS",
  "database": "AdventureWorks2022",
  "trusted_connection": true
}


👉 Byt ut server mot din instans och anpassa trusted_connection till false om du vill använda användarnamn/lösenord.

▶️ Körning

Starta ETL-processen med:

python etl/main.py


Processen gör då:

Extract – hämtar försäljningsdata från AdventureWorks2022.

Transform – standardiserar kundnamn, konverterar datatyper och rensar kolumner.

Load – sparar resultatet som CSV i output/sales_data.csv.

📊 Resultat

Outputen är en CSV-fil som kan importeras direkt till Power BI eller andra analysverktyg.

Loggar skrivs till logs/etl_log.txt och logs/etl_error_log.txt.

📈 Power BI-rapport

Detta repo innehåller även en Power BI-rapport byggd på försäljningsdatan från ETL-flödet.
Rapporten visar bland annat:

Försäljning per land, region och stad

Toppsäljande produkter

Total försäljning över tid

Kundsegmentering (personer vs butiker)

🔗 Användning

Kör ETL-processen för att generera en färsk sales_data.csv i output/.

Öppna Power BI Desktop och ladda in sales_data.csv.

Uppdatera rapporten med senaste data.

(Om du har sparat .pbix-filen i mappen reports/ kan du öppna den direkt och bara klicka Refresh).
