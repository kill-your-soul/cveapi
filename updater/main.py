import hashlib
import json
import re
import time
from io import BytesIO

import click
import requests
from openpyxl import load_workbook

from config import settings

# from models import Nvd

@click.command()
def init_bdu():
    print("Getting info from BDU")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }
    xlsx = requests.get(settings.BDU_XLSX_URL, verify=False, allow_redirects=True, headers=headers).content  # noqa: S113, S501
    wb = load_workbook(filename=BytesIO(xlsx))
    results = []
    sheet = wb.active
    for row in sheet.iter_rows(min_row=3):
        bdu_id = row[0].value
        description = row[1].value
        bdu_data = {"cve_id": "", "bdu_id": bdu_id, "description": description}
        other_id = row[18].value
        # print(f"{other_id =}")
        if other_id:
            cve_match = re.findall(r"CVE-\d{4}-\d{4}", str(other_id))
            # print(cve_match)
            for cve_id in cve_match:
                bdu_data["cve_id"] = cve_id
                results.append(bdu_data)
        else:
            bdu_data["cve_id"] = ""
            results.append(bdu_data)
    for bdu in results:
        resp = requests.post(settings.CVE_API_URL + "api/v1/bdu/", data=json.dumps(bdu))
        print(resp.text)


@click.command()
def init_nvd() -> None:
    """Import the CVE list.

    Important notice:
        This product uses data from the NVD API but is not endorsed or certified by the NVD.
    """
    print("Gettins info from NVD")  # noqa: T201
    mappings = {"vendors": {}, "products": {}, "cves": [], "changes": []}
    url_template = settings.NVD_API_URL + "?startIndex={idx}"

    start_index = 0
    total_results = 0

    while start_index <= total_results:
        url = url_template.format(idx=start_index)
        # with timed_operation(f"Downloading {url}"):
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
                # id=cve_db_id,  # noqa: ERA001
                cve_id=cve_id,
                summary=summary,
                json=cve_data,
                vendors=vendors_products,
                cwes=cwes,
                cvss2=cvss2,
                cvss3=cvss3,
                # created_at=arrow.get(cve_data["published"]).datetime,  # noqa: ERA001
                # updated_at=arrow.get(cve_data["lastModified"]).datetime,  # noqa: ERA001
            )
            # Create the CVEs mappings
            mappings["cves"].append(
                cve,
            )
            # nvd_in = NvdCreat(**cve)
            # nvd_in_hash_sum = hashlib.sha256(json.dumps(nvd_in.model_dump(), sort_keys=True).encode("utf-8")).hexdigest()
            # print(nvd_in_hash_sum)
            # print(cve)
            break

        # NVD requirement is 2000 CVE per page
        start_index += 2000

        # Insert the objects in database
        if (start_index % 20_000 == 0) or (start_index >= total_results):
            # with timed_operation("Inserting CVE"):
            # db.session.bulk_insert_mappings(Cve, mappings["cves"])
            # db.session.commit()
            # Create the changes based on CVEs data
            for cve in mappings["cves"]:
                print(cve)
                resp = requests.post(settings.CVE_API_URL + "api/v1/nvd/", data=json.dumps(cve))
                print(resp.text)
                # time.sleep(1)
                # mappings["changes"].append(
                #     dict(
                #         id=get_uuid(),
                #         created_at=cve["created_at"],
                #         updated_at=cve["updated_at"],
                #         json=cve["json"],
                #         cve_id=cve["id"],
                #         task_id=task_id,
                #     )
                # )
            # db.session.bulk_insert_mappings(Change, mappings["changes"])
            # db.session.commit()

            # info("{} CVE imported.".format(len(mappings["cves"])))

            # Free the memory after each processed year
            mappings["cves"] = []
            mappings["changes"] = []

        # NVD requirement is 6s between requests
        if start_index <= total_results:
            # info("Waiting 6 seconds")
            time.sleep(6)


if __name__ == "__main__":
    init_bdu()
