from config import settings
import time
import requests
import json
from openpyxl import load_workbook
from io import BytesIO


def run_bdu():
    print("Getting info from BDU")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }
    xlsx = requests.get(settings.BDU_XLSX_URL, verify=False, allow_redirects=True, headers=headers).content
    wb = load_workbook(filename=BytesIO(xlsx))


def run_nvd():
    """
    Import the CVE list.

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
        # with timed_operation(f"Downloading {url}"):
        print(f"Downloading {url}")
        resp = requests.get(url)

        if not resp.ok:
            print(f"Bad response: {resp.status_code}, sleeping before retrying")
            time.sleep(10)
            continue

        # with timed_operation("Creating model objects"):
        data = resp.json()
        total_results = data.get("totalResults")
        for vulnerability in data.get("vulnerabilities"):
            # cve_db_id = get_uuid()

            cve_data = vulnerability.get("cve")
            cve_id = cve_data["id"]

            # Takes the CVSS scores
            if "cvssMetricV31" in cve_data["metrics"]:
                cvss3 = cve_data.get("metrics")["cvssMetricV31"][0]["cvssData"][
                    "baseScore"
                ]
            elif "cvssMetricV30" in cve_data["metrics"]:
                cvss3 = cve_data.get("metrics")["cvssMetricV30"][0]["cvssData"][
                    "baseScore"
                ]
            else:
                cvss3 = 0

            if "cvssMetricV2" in cve_data.get("metrics"):
                cvss2 = cve_data.get("metrics")["cvssMetricV2"][0]["cvssData"][
                    "baseScore"
                ]
            else:
                cvss2 = 0

            # Construct CWE and CPE lists
            # cwes = cve_data.get("weaknesses", {})
            if "weaknesses" in cve_data:
                cwes = cve_data["weaknesses"][0]
            else:
                cwes = {}
            # print(cwes)
            # vendors_products = cve_data.get("configurations", {})
            # print((vendors_products))
            if "configurations" in cve_data:
                vendors_products = cve_data["configurations"][0]
            else:
                vendors_products = {}
            # In case of multiple languages, keep the EN one
            descriptions = cve_data["descriptions"]
            if len(descriptions) > 1:
                descriptions = [
                    d for d in descriptions if d["lang"] in ("en", "en-US")
                ]
            summary = descriptions[0]["value"]

            # Create the CVEs mappings
            mappings["cves"].append(
                dict(
                    # id=cve_db_id,
                    cve_id=cve_id,
                    summary=summary,
                    json=cve_data,
                    vendors=vendors_products,
                    cwes=cwes,
                    cvss2=cvss2,
                    cvss3=cvss3,
                    # created_at=arrow.get(cve_data["published"]).datetime,
                    # updated_at=arrow.get(cve_data["lastModified"]).datetime,
                )
            )

            # Create the vendors and their products
            # for vendor, products in vendors_products.items():

            #     # Create the vendor
            #     if vendor not in mappings["vendors"].keys():
            #         mappings["vendors"][vendor] = dict(id=get_uuid(), name=vendor)

            #     for product in products:
            #         if get_slug(vendor, product) not in mappings["products"].keys():
            #             mappings["products"][get_slug(vendor, product)] = dict(
            #                 id=get_uuid(),
            #                 name=product,
            #                 vendor_id=mappings["vendors"][vendor]["id"],
            #             )

        # NVD requirement is 2000 CVE per page
        start_index += 2000

        # Insert the objects in database
        if (start_index % 20_000 == 0) or (start_index >= total_results):
            # with timed_operation("Inserting CVE"):
            # db.session.bulk_insert_mappings(Cve, mappings["cves"])
            # db.session.commit()
            # Create the changes based on CVEs data
            for cve in mappings["cves"]:
                # print(cve)
                resp = requests.post(settings.CVE_API_URL+"api/v1/nvd/", data=json.dumps(cve))
                # print(resp.text)
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

    # Save the last CVE in database (will be reused in the handle_events task
    # with timed_operation("Saving last CVE information"):
    # last_cve = Cve.query.order_by(Cve.updated_at.desc()).first()
    # db.session.add(Meta(name="nvd_last_cve_id", value=str(last_cve.cve_id)))
    # db.session.add(
    #     Meta(name="nvd_last_cve_updated_at", value=str(last_cve.updated_at))
    # )
    # db.session.commit()

    # Insert the objects in database
    # with timed_operation("Inserting Vendors and Products"):
    # db.session.bulk_insert_mappings(Vendor, mappings["vendors"].values())
    # db.session.bulk_insert_mappings(Product, mappings["products"].values())
    # db.session.commit()


if __name__ == '__main__':
    run_nvd()