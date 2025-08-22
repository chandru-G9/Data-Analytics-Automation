import os
import subprocess
import logging
from datetime import datetime
import json

# ----------------- Load config -----------------
config_path = r"C:\Users\chand\OneDrive\Desktop\Data analytics\Configuration\config.json"
with open(config_path) as f:
    config = json.load(f)
    log_dir = config["paths"]["log_folder"]
    scripts = config["scripts"]


# Log file path
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "run_all.log")

# Configure logging (HH:MM:SS format, no timezone)
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Scripts to run (absolute paths)
scripts = [
    scripts["etl"],
    scripts["report"],
    scripts["mail"]
]

def run_script(script_name):
    """Run a Python script and log the output."""
    try:
        logging.info(f"Starting {script_name}")
        result = subprocess.run(
            ["python", script_name],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            logging.info(f"{script_name} finished successfully")
            if result.stdout.strip():
                logging.info(f"{script_name} output:\n{result.stdout.strip()}")
        else:
            logging.error(f"{script_name} failed with error code {result.returncode}")
            if result.stderr.strip():
                logging.error(f"{script_name} error output:\n{result.stderr.strip()}")
    except Exception as e:
        logging.exception(f"Exception while running {script_name}: {e}")

def main():
    logging.info("=== Run started ===")
    for script in scripts:
        run_script(script)
    logging.info("=== Run finished ===")

if __name__ == "__main__":
    main()
