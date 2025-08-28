Automated Sales ETL & Reporting Project
Overview
This project is an end-to-end automated ETL and reporting pipeline built in Python. It extracts sales data from CSV, loads it into a SQL Server fact table, generates KPI reports as Excel files, compresses them into a ZIP, and finally emails them to recipients.
The entire process is scheduled to run daily on a local machine using Windows Task Scheduler.

Project Workflow
ETL Script (etl.py)
Reads a CSV sales dataset.
Cleans and transforms the data.
Loads new rows into SQL Server (dbo.fact_sales).

Report Generation (report.py)
Reads pre-written SQL queries from .sql files.
Executes queries against SQL Server.
Saves results as Excel reports, organized by category.

Email Script (mail.py)
Compresses all Excel reports into a single ZIP.
Attaches reports + log file.
Sends them via Gmail SMTP to configured recipients.

Master Runner (run_all.py)
Sequentially runs ETL → Report → Mail.
Centralized logging for execution monitoring.
This script is scheduled to run daily.

Folder Structure
The project uses paths defined in config.json. Example structure:

Data analytics/
│
├── Configuration/
│   └── config.json
│
├── Logs/                 # Auto-created, contains log files
│   ├── etl.log
│   ├── report_generation.log
│   ├── email_log.log
│   └── run_all.log
│
├── Reports/              # Auto-created, contains KPI reports
│   ├── Sales/
│   │   ├── Total_Sales.xlsx
│   │   └── Top_Customers.xlsx
│   └── Customers/
│       └── Active_Customers.xlsx
│
├── SQL/                  # Folder containing query files
│   ├── sales_kpis.sql
│   └── customer_kpis.sql
│
├── Scripts/              # Python scripts
│   ├── etl.py
│   ├── report.py
│   ├── mail.py
│   └── run_all.py

Logging
Logging is implemented in every script to track execution and errors.
ETL logs → etl.log
Report logs → report_generation.log
Email logs → email_log.log
Master run logs → run_all.log

Logs capture:
Script start/finish
Number of rows inserted
Reports generated successfully
Emails sent or errors encountered

SQL Reports
Each .sql file in the SQL/ folder can contain multiple queries separated by --.
The first line after -- is treated as the KPI name.
Each KPI is saved as a separate Excel file in a subfolder named after the .sql file.

Example (sales_kpis.sql):
-- Total_Sales
SELECT SUM(sales_amount) AS total_sales FROM dbo.fact_sales;

-- Top_Customers
SELECT TOP 10 customer_key, SUM(sales_amount) AS total_sales
FROM dbo.fact_sales
GROUP BY customer_key
ORDER BY total_sales DESC;


This would generate:
Reports/Sales/Total_Sales.xlsx  
Reports/Sales/Top_Customers.xlsx  

Email Automation
All Excel reports are compressed into Reports_Attachments.zip.
The report log file (report_generation.log) is also attached.
Email is sent via Gmail SMTP.
Multiple recipients supported.

Scheduling
The pipeline is automated using Windows Task Scheduler.
The scheduled task runs run_all.py daily at a specified time.

This ensures:
Fresh data is loaded.
Reports are regenerated.
Emails are delivered automatically.

Key Features
✅ Fully automated ETL + reporting + email pipeline
✅ Config-driven (no hardcoded paths or credentials)
✅ Logs every step for audit & debugging
✅ Excel-based reporting for business users
✅ Works with SQL Server via sqlalchemy + pyodbc
✅ Scheduled with Windows Task Scheduler
