import os
import tempfile
from pathlib import Path
from sys import platform


def get_project_root_dir() -> Path:
    return Path(__file__).parent.parent


def create_and_get_config_directory(logger) -> Path:
    try:
        if platform == "win32":  # Windows
            env_path = Path(os.getenv("APPDATA")) / "nvd_cve_retriever" / "config"
        else:  # Unix/Linux/macOS
            env_path = Path.home() / ".nvd_cve_retriever" / "config"

        env_path.mkdir(parents=True, exist_ok=True)
        return env_path
    except Exception as e:
        fallback_path = Path(tempfile.gettempdir()) / "nvd_cve_retriever" / "config"
        logger.error(
            f"Erreur lors de la création du répertoire de configuration : {e} - Utilisation du répertoire de repli : {fallback_path}"
        )
        return fallback_path


def create_and_get_log_directory(logger) -> Path:
    try:
        if platform == "win32":  # Windows
            log_directory = Path(os.getenv("APPDATA")) / "nvd_cve_retriever" / "logs"
        else:  # Unix/Linux/macOS
            log_directory = Path.home() / ".nvd_cve_retriever" / "logs"

        log_directory.mkdir(parents=True, exist_ok=True)
        return log_directory
    except Exception as e:
        fallback_path = Path(tempfile.gettempdir()) / "nvd_cve_retriever" / "logs"
        logger.error(
            f"Erreur lors de la création du répertoire de log : {e} - Utilisation du répertoire de repli : {fallback_path}"
        )
        return fallback_path


def create_and_get_output_directory(logger) -> Path:
    try:
        if platform == "win32":  # Windows
            output_directory = (
                Path(os.getenv("APPDATA")) / "nvd_cve_retriever" / "outputs"
            )
        else:  # Unix/Linux/macOS
            output_directory = Path.home() / ".nvd_cve_retriever" / "outputs"

        output_directory.mkdir(parents=True, exist_ok=True)
        return output_directory
    except Exception as e:
        fallback_path = Path(tempfile.gettempdir()) / "nvd_cve_retriever" / "logs"
        logger.error(
            f"Erreur lors de la création du répertoire de sortie des fichiers JSON et TXT : {e} - Utilisation du répertoire de repli : {fallback_path}"
        )
        return fallback_path
