import os
from pathlib import Path

CONFIG_DIR = Path.home() / ".ctfpilot"
CONFIG_FILE = CONFIG_DIR / "config.env"

def get_groq_key() -> str | None:
    # 1. Busca en variable de entorno del sistema
    key = os.environ.get("GROQ_API_KEY")
    if key:
        return key
    # 2. Busca en archivo de configuracion local
    if CONFIG_FILE.exists():
        for line in CONFIG_FILE.read_text().splitlines():
            if line.startswith("GROQ_API_KEY="):
                return line.split("=", 1)[1].strip()
    return None

def save_groq_key(key: str):
    CONFIG_DIR.mkdir(exist_ok=True)
    CONFIG_FILE.write_text(f"GROQ_API_KEY={key}\n")
    CONFIG_FILE.chmod(0o600)