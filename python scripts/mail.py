import os
import smtplib
import zipfile
from email.message import EmailMessage
from datetime import datetime
import logging
import json

# ----------------- Load config -----------------
config_path = r"C:\Users\chand\OneDrive\Desktop\Data analytics\Configuration\config.json"
with open(config_path) as f:
    config = json.load(f)
    SENDER_PASSWORD = config["email"]["password"]
    LOG_FOLDER = config["paths"]["log_folder"]
    REPORTS_FOLDER = config["paths"]["report_folder"]
    SENDER_EMAIL = config["email"]["sender"]
    RECIPIENTS = config["email"]["receivers"]

# ---------------- CONFIG ----------------
REPORT_LOG_FILE = os.path.join(LOG_FOLDER, "report_generation.log")
EMAIL_LOG_FILE = os.path.join(LOG_FOLDER, "email_log.log")
ZIP_FILENAME = os.path.join(LOG_FOLDER, "Reports_Attachments.zip")


SUBJECT = "Automated Report with Logs"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587  # TLS

# ---------------- LOGGING SETUP ----------------
logging.basicConfig(
    filename=EMAIL_LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------------- CREATE ZIP ----------------
def create_zip_of_reports(reports_folder, zip_filename):
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(reports_folder):
            for file in files:
                if file.endswith(".xlsx"):
                    filepath = os.path.join(root, file)
                    arcname = os.path.relpath(filepath, reports_folder)  # keep folder structure
                    zipf.write(filepath, arcname)
                    logging.info(f"{file} zipped")
    logging.info(f"Zipped all reports into {zip_filename}")

# ---------------- SEND EMAIL ----------------
def send_email():
    try:
        msg = EmailMessage()
        msg["Subject"] = SUBJECT
        msg["From"] = SENDER_EMAIL
        msg["To"] = ", ".join(RECIPIENTS)
        msg.set_content("Please find attached the zipped reports and the log file.")

        # 1. Attach the ZIP of reports
        if os.path.exists(ZIP_FILENAME):
            with open(ZIP_FILENAME, "rb") as f:
                msg.add_attachment(f.read(),
                                   maintype="application",
                                   subtype="zip",
                                   filename=os.path.basename(ZIP_FILENAME))
            logging.info(f"Attached ZIP: {ZIP_FILENAME}")
        else:
            logging.warning("ZIP file not found, skipping attachment.")

        # 2. Attach the report_generation.log file
        if os.path.exists(REPORT_LOG_FILE):
            with open(REPORT_LOG_FILE, "rb") as f:
                msg.add_attachment(f.read(),
                                   maintype="text",
                                   subtype="plain",
                                   filename=os.path.basename(REPORT_LOG_FILE))
            logging.info(f"Attached log: {REPORT_LOG_FILE}")
        else:
            logging.warning("Report log file not found, skipping attachment.")

        # Send email using STARTTLS
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        logging.info(f"Email sent successfully to {RECIPIENTS}")

    except Exception as e:
        logging.error(f"Error while sending email: {e}")

# ---------------- MAIN ----------------
if __name__ == "__main__":
    logging.info("----- Email Script Started -----")
    create_zip_of_reports(REPORTS_FOLDER, ZIP_FILENAME)
    send_email()
    logging.info("----- Email Script Finished -----\n")
