import os
import requests
import json
import datetime
from pathlib import Path
from dotenv import load_dotenv
from argparse import ArgumentParser, Namespace
from typing import Dict, List, Optional, Any

from nvd_cve_retriever.utils.utils import (
    create_and_get_output_directory,
    create_and_get_config_directory,
)
from nvd_cve_retriever.cve_fetcher.fetcher import CVEFetcher
from nvd_cve_retriever.cve_fetcher.formatter import format_to_text, format_to_json
from nvd_cve_retriever.logs.logger import configure_logging, ColoredLogger


def main() -> None:
    args: Namespace = parse_arguments()
    logger: ColoredLogger = ColoredLogger(args.verbose)
    configure_logging(args.verbose)

    config_dir: Path = create_and_get_config_directory(logger)
    load_dotenv(dotenv_path=str(f"{config_dir}/.env"))

    logger.info("Démarrage du programme...")

    api_profile_configuration: Dict[str, Optional[str]] = {
        "api_key": os.getenv("NVD_API_KEY"),
        "api_url": os.getenv("NVD_API_URL"),
    }

    if not all(api_profile_configuration.values()):
        api_profile_configuration: Dict[str, str] = ask_for_api_profile_configuration(
            logger
        )

    fetcher: CVEFetcher = CVEFetcher(
        api_profile_configuration["api_key"], api_profile_configuration["api_url"]
    )
    cves: List[Dict[str, Any]] = fetcher.grab_cves(args.days, logger)

    if cves:
        save_results(
            cves,
            args.verbose,
            args.output
            if args.output
            else str(create_and_get_output_directory(logger)),
        )
    else:
        logger.error("Les résultats n'ont pas pu être sauvegardés")


def is_valid_api_key(api_key: str) -> bool:
    api_url: str = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    headers: Dict[str, str] = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "apiKey": api_key,
    }
    try:
        response = requests.get(api_url, headers=headers)
        if (
            response.raise_for_status()
        ):  # Déclenchera une exception pour les réponses 4xx/5xx
            return False
        return True  # Si la requête est réussie, on considère la clé comme valide
    except requests.RequestException:
        return False  # En cas d'erreur de requête, on considère la clé comme invalide


def ask_for_api_profile_configuration(logger: ColoredLogger) -> Dict[str, str]:
    while True:
        api_key: str = input("Veuillez entrer votre clé API NVD : ")
        if is_valid_api_key(api_key):
            logger.success("Votre clé pour l'API NVD a été validée.")
            break
        else:
            logger.warning("La clé API fournie est invalide. Veuillez réessayer.")

    api_profile_configuration: Dict[str, str] = {
        "api_key": api_key,
        "api_url": "https://services.nvd.nist.gov/rest/json/cves/2.0",
    }

    config_dir: Path = create_and_get_config_directory(logger)

    try:
        with open(f"{config_dir}/.env", "w") as env_file:
            env_file.write(f"NVD_API_KEY={api_profile_configuration['api_key']}\n")
            env_file.write(f"NVD_API_URL={api_profile_configuration['api_url']}\n")
        logger.success("Configuration créée avec succès.")
    except IOError as e:
        logger.error(f"Erreur lors de la création de votre configuration : {e}")

    return api_profile_configuration


def parse_arguments() -> Namespace:
    temp_logger = ColoredLogger(verbose=False)
    parser: ArgumentParser = ArgumentParser(description="NVD CVE Grabber Tool")

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.1",
        help="Affiche la version actuelle.",
    )
    parser.add_argument(
        "-d", "--days", type=int, default=1, help="Nombre de jours pour fetch les CVEs."
    )
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Augmenter la verbosité."
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=str(create_and_get_output_directory(temp_logger)),
        help="Chemin du répertoire de sortie des fichiers.",
    )

    return parser.parse_args()


def save_results(cves: List[Dict[str, Any]], verbose: bool, output_dir: str) -> None:
    logger: ColoredLogger = ColoredLogger(verbose)

    # Utiliser le répertoire de sortie spécifié ou le répertoire par défaut
    output_dir_path: Path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    # Créer un sous-dossier avec la date actuelle pour les fichiers outputs
    date_str: str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_subdir: str = os.path.join(output_dir, date_str)
    os.makedirs(output_subdir, exist_ok=True)

    # Formatter et sauvegarder dans un fichier JSON
    json_path: str = os.path.join(output_subdir, f"{date_str}.json")
    with open(json_path, "w") as json_file:
        json.dump(format_to_json(cves, logger), json_file, indent=4)
    logger.success("Fichier JSON généré")

    # Formatter et sauvegarder dans un fichier TXT
    text_path: str = os.path.join(output_subdir, f"{date_str}.txt")
    with open(text_path, "w") as text_file:
        text_file.write(format_to_text(cves, logger))

    logger.success("Fichier TXT généré")
    logger.success(f"Résultats sauvegardés dans {output_subdir}")


if __name__ == "__main__":
    main()
