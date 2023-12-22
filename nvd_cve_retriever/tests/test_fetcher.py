import unittest
from unittest.mock import patch
from nvd_cve_retriever.cve_fetcher.fetcher import CVEFetcher


class TestCVEFetcher(unittest.TestCase):
    def setUp(self):
        self.api_key = "dummy_api_key"
        self.base_url = "http://example.com"
        self.fetcher = CVEFetcher(api_key=self.api_key, base_url=self.base_url)

    @patch("cve_fetcher.fetcher.requests.get")
    def test_grab_cves_successful(self, mock_get):
        # Simuler une réponse de l'API réussie
        mock_response = mock_get.return_value
        mock_response.json.return_value = {
            "result": {
                "CVE_Items": [
                    # TODO: Remplir les items pour simuler l'affichage du json
                ]
            }
        }
        mock_response.status_code = 200

        cves = self.fetcher.grab_cves(1)
        self.assertIsInstance(cves, list)

    @patch("cve_fetcher.fetcher.requests.get")
    def test_grab_cves_failure(self, mock_get):
        # Simuler un échec de réponse de l'API
        mock_get.side_effect = Exception("Requête à l'API échouée")

        cves = self.fetcher.grab_cves(1)
        self.assertEqual(cves, [])


if __name__ == "__main__":
    unittest.main()
