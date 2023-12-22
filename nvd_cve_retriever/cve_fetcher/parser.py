def parse_cve_response(response, logger):
    """
    Parse les données de la réponse API.
    """
    try:
        filtered_vulns = [
            vuln
            for vuln in response["vulnerabilities"]
            if vuln["cve"]["vulnStatus"] == "Analyzed"
        ]

        parsed_cves = []
        for vuln in filtered_vulns:
            parsed_cve = {
                "CVE_ID": vuln["cve"]["id"],
                "Published": vuln["cve"]["published"],
                "Last_Modified": vuln["cve"]["lastModified"],
                "Description": vuln["cve"]["descriptions"][0]["value"],
                "Lien vers NVD": f"https://nvd.nist.gov/vuln/detail/{vuln['cve']['id']}",
            }
            parsed_cves.append(parsed_cve)

        return parsed_cves

    except Exception as e:
        logger.error(f"Erreur rencontrée lors du parsing de la réponse : {e}")
        return []
