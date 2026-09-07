import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "database", "siem.db")
SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "development-only-secret")
MAX_CONTENT_LENGTH = 1024 * 1024
