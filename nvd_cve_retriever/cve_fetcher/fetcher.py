import requests

from datetime import date, timedelta
from typing import List, Dict, Optional, Any
from nvd_cve_retriever.logs.logger_interface import ILogger
from nvd_cve_retriever.cve_fetcher.parser import parse_cve_response


class CVEFetcher:
    def __init__(self, api_key: str, base_url: str):
        self.api_key: str = api_key
        self.base_url: str = base_url

    def grab_cves(self, days: int, logger: ILogger) -> Optional[List[Dict[str, Any]]]:
        start_date, end_date = self._calculate_dates(days)
        api_url: str = f"{self.base_url}/?pubStartDate={start_date}&pubEndDate={end_date}&noRejected"
        headers: Dict[str, str] = self._prepare_headers()
        response: Optional[Dict[str, Any]] = self._make_request(
            api_url, headers, logger
        )

        if response:
            logger.success(f"Contenu récupéré via l'API de NVD ({api_url})")
            return parse_cve_response(response, logger)
        else:
            logger.error("Il y a eu une erreur lors de la requête à l'API de NVD")
            return None

    def _calculate_dates(self, days: int) -> (str, str):
        today: date = date.today()
        delta: timedelta = timedelta(days=days)
        start_date: str = (today - delta).isoformat() + "T00:00:00.000-01:00"
        end_date: str = today.isoformat() + "T23:59:59.999-01:00"

        return start_date, end_date

    def _prepare_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "apiKey": self.api_key,
        }

    def _make_request(
        self, url: str, headers: Dict[str, str], logger: ILogger
    ) -> Optional[Dict[str, Any]]:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Déclenchera une exception pour les réponses 4xx/5xx

            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur rencontrée en faisant la requête à l'API NVD : {e}")
            return None
