import os
from pathlib import Path
from dotenv import load_dotenv

# Base project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env if present
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# Gemini API configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-pro").strip()

# Server configuration
BACKEND_HOST = os.getenv("BACKEND_HOST", "127.0.0.1")
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))
BACKEND_URL = os.getenv("BACKEND_URL", f"http://{BACKEND_HOST}:{BACKEND_PORT}").rstrip("/")

# Asset paths
ASSETS_DIR = BASE_DIR / "assets"
LOGO_DIR = ASSETS_DIR / "logo"
DEFAULT_LOGO_PATH = LOGO_DIR / "logo.png"
INVERSE_LOGO_PATH = LOGO_DIR / "inverseLogo.png"

# App Metadata
APP_NAME = "LegalEase"
APP_SUBTITLE = "AI-Powered Legal Document Generator"
LEGAL_DISCLAIMER = (
    "LegalEase provides AI-generated draft documents and legal information for general "
    "informational purposes. It does not constitute legal advice and should not replace "
    "review by a qualified legal professional."
)


def is_gemini_configured() -> bool:
    """Check if a non-empty Gemini API key is configured."""
    return bool(GEMINI_API_KEY and len(GEMINI_API_KEY) > 5)
