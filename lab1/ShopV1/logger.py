import logging
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE_PATH = os.path.join(BASE_DIR, "logs", "server.log")

if not os.path.exists(LOG_FILE_PATH):
    parent_dir = os.path.dirname(BASE_DIR)
    LOG_FILE_PATH = os.path.join(parent_dir, "logs", "server.log")

logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)
