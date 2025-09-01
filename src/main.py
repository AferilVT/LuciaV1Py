import os
import sys
import logging
from dotenv import load_dotenv
from typing import Optional

# --- Utility functions ---
def get_project_root() -> str:
    """Return the absolute path to the project root (one level above src)."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def get_env_path() -> str:
    """Return the absolute path to the .env file in the project root."""
    return os.path.join(get_project_root(), '.env')

def get_log_path() -> str:
    """Return the absolute path to the log file in the logs directory in the project root."""
    log_dir = os.path.join(get_project_root(), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    return os.path.join(log_dir, 'lucia.log')

# --- Logging setup ---
log_file = get_log_path()
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

# --- Environment loading ---
env_path = get_env_path()
if not os.path.exists(env_path):
    logging.error(f".env file not found at: {env_path}")
    print(f"Error: .env file not found at: {env_path}")
    print("Please ensure the .env file exists in the project root directory.")
    input("Press Enter to exit...")
    sys.exit(1)

load_dotenv(env_path)
token: Optional[str] = os.getenv("TOKEN")
if not token:
    logging.error("TOKEN not found in .env file.")
    print("Error: TOKEN not found in .env file.")
    print("Please ensure the .env file contains a valid Discord bot token.")
    input("Press Enter to exit...")
    sys.exit(1)

# --- Bot startup ---
from lucia import Lucia

def main() -> None:
    try:
        logging.info("Starting Lucia Discord bot...")
        bot = Lucia()
        bot.run(token)
    except Exception as e:
        logging.exception("Failed to start Lucia bot")
        print(f"Error: Failed to start Lucia bot - {e}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
