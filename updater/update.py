import hashlib
import json
import time

import requests  # type: ignore  # noqa: PGH003

from config import celery, settings
from models import Nvd


@celery.task
def update_bdu() -> None:
    # TODO @kill_your_soul: Add update bdu
    pass


@celery.task
def update_nvd() -> None:  # noqa: PLR0915, PLR0912, C901
    """Import the CVE list.

    Important notice:
        This product uses data from the NVD API but is not endorsed or certified by the NVD.
    """
    print("Gettins info from NVD")
    mappings = {"vendors": {}, "products": {}, "cves": [], "changes": []}
    url_template = settings.NVD_API_URL + "?startIndex={idx}"

    start_index = 0
    total_results = 0

    while start_index <= total_results:
        url = url_template.format(idx=start_index)
        print(f"Downloading {url}")
        resp = requests.get(url)

        if not resp.ok:
            print(f"Bad response: {resp.status_code}, sleeping before retrying")
            time.sleep(10)
            continue
        data = resp.json()
        total_results = data.get("totalResults")
        for vulnerability in data.get("vulnerabilities"):
            cve_data = vulnerability.get("cve")
            cve_id = cve_data["id"]
            if "cvssMetricV31" in cve_data["metrics"]:
                cvss3 = cve_data.get("metrics")["cvssMetricV31"][0]["cvssData"]["baseScore"]
            elif "cvssMetricV30" in cve_data["metrics"]:
                cvss3 = cve_data.get("metrics")["cvssMetricV30"][0]["cvssData"]["baseScore"]
            else:
                cvss3 = 0

            if "cvssMetricV2" in cve_data.get("metrics"):
                cvss2 = cve_data.get("metrics")["cvssMetricV2"][0]["cvssData"]["baseScore"]
            else:
                cvss2 = 0
            if "weaknesses" in cve_data:
                cwes = cve_data["weaknesses"][0]
            else:
                cwes = {}

            if "configurations" in cve_data:
                vendors_products = cve_data["configurations"][0]
            else:
                vendors_products = {}
            # In case of multiple languages, keep the EN one
            descriptions = cve_data["descriptions"]
            if len(descriptions) > 1:
                descriptions = [d for d in descriptions if d["lang"] in ("en", "en-US")]
            summary = descriptions[0]["value"]
            cve = dict(  # noqa: C408
                cve_id=cve_id,
                summary=summary,
                json=cve_data,
                vendors=vendors_products,
                cwes=cwes,
                cvss2=cvss2,
                cvss3=cvss3,
            )
            # Create the CVEs mappings
            mappings["cves"].append(
                cve,
            )

        start_index += 2000

        # Update the objects in database
        if (start_index % 20_000 == 0) or (start_index >= total_results):
            for cve in mappings["cves"]:
                nvd_in = Nvd(**cve)
                nvd_in_hash_sum = hashlib.sha256(
                    json.dumps(nvd_in.model_dump(), sort_keys=True).encode("utf-8"),
                ).hexdigest()
                print(nvd_in_hash_sum)
                server_data = requests.get(settings.CVE_API_URL + f"api/v1/cve/?cve_id={cve['cve_id']}").json()
                print(server_data["nvd"]["hash_sum"])
                if server_data["nvd"]["hash_sum"] != nvd_in_hash_sum:
                    print("New data")
                    resp = requests.put(
                        settings.CVE_API_URL + f'api/v1/nvd/{server_data["nvd"]["id"]}',
                        data=json.dumps(cve),
                    )
                    print(resp.text)
                else:
                    print("Old data")
            mappings["cves"] = []
            mappings["changes"] = []

        if start_index <= total_results:
            # info("Waiting 6 seconds")
            time.sleep(6)


@celery.task
def update() -> None:
    update_nvd()
    update_bdu()
