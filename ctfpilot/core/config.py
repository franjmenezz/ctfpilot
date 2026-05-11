import os
from pathlib import Path

def get_config_dir() -> Path:
    # Si se ejecuta con sudo, usa el home del usuario real
    sudo_user = os.environ.get("SUDO_USER")
    if sudo_user:
        return Path(f"/home/{sudo_user}") / ".ctfpilot"
    return Path.home() / ".ctfpilot"

def get_groq_key() -> str | None:
    config_file = get_config_dir() / "config.env"
    # 1. Busca en variable de entorno del sistema
    key = os.environ.get("GROQ_API_KEY")
    if key:
        return key
    # 2. Busca en archivo de configuracion local
    if config_file.exists():
        for line in config_file.read_text().splitlines():
            if line.startswith("GROQ_API_KEY="):
                return line.split("=", 1)[1].strip()
    return None

def save_groq_key(key: str):
    config_dir = get_config_dir()
    config_dir.mkdir(exist_ok=True)
    config_file = config_dir / "config.env"
    config_file.write_text(f"GROQ_API_KEY={key}\n")
    config_file.chmod(0o600)