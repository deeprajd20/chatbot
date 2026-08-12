from pathlib import Path


# =========================================================
# PROJECT PATHS
# =========================================================

# src/config.py
#      ↓ parent
# src/
#      ↓ parent
# chatbot/

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================================================
# APPLICATION DIRECTORIES
# =========================================================

SESSION_CHATS_DIR = BASE_DIR / "session_chats"

TEMPLATES_DIR = BASE_DIR / "src" / "templates"


# =========================================================
# CREATE REQUIRED DIRECTORIES
# =========================================================

SESSION_CHATS_DIR.mkdir(parents=True, exist_ok=True)

print(SESSION_CHATS_DIR, TEMPLATES_DIR)
