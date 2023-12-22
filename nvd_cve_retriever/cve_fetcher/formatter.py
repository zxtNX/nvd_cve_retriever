def format_to_json(cves, logger):
    # On assume que les CVEs sont déjà dans un format compatible JSON
    logger.success("Formattage JSON réalisé")
    return cves


def format_to_text(cves, logger):
    """
    Formattage CVEs dans un format text avec une série de blocs
    Chaque bloc contient les détails d'une CVE avec ses champs
    On a choisi cette méthhode d'affichage au lieu d'un tableau / grid car elle a l'avantage
    de ne pas casser les lignes à cause de la description trop longue
    """
    try:
        text_output = []

        for cve in cves:
            block = (
                f"CVE_ID: {cve['CVE_ID']}\n"
                f"Published: {cve['Published']}\n"
                f"Last_Modified: {cve['Last_Modified']}\n"
                f"Description: {cve['Description']}\n"
                "Lien vers NVD:"
                f" https://nvd.nist.gov/vuln/detail/{cve['CVE_ID']}\n\n"
                "----------------------------------------"
            )

            text_output.append(block)

        logger.success("Formattage TXT réalisé")
        return "\n\n".join(text_output)

    except Exception as e:
        logger.error(f"Erreur rencontrée lors du formattage pour le format TXT : {e}")
        return []
