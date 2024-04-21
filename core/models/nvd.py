from sqlalchemy import JSON
from sqlmodel import Column, Field, MetaData

from models.base import BaseModel


class Nvd(BaseModel, table=True):
    metadata = MetaData()
    __tablename__ = "nvds"

    cve_id: str = Field(nullable=False)
    json: dict = Field(sa_column=Column(JSON), default={})

    # We used initially secondary relationships to fetch the list of
    # associated vendors, products and cwes. But it was complicated
    # to maintain, and the performance were poor. So we now use the
    # JSONB data type associated to the GIN index type.
    vendors: dict = Field(sa_column=Column(JSON), default={})
    cwes: dict = Field(sa_column=Column(JSON), default={})

    # Keep the summary separated when searching keywords
    summary: str = Field(nullable=False)

    # Keep CVSS separated when searching a particular score
    cvss2: float = Field(nullable=True)
    cvss3: float = Field(nullable=True)

    @property
    def cvss2_score(self):  # noqa: ANN201
        if "cve" in self.json.keys():  # noqa: SIM118
            if "baseMetricV2" in self.json["impact"]:
                return self.json["impact"]["baseMetricV2"]["cvssV2"]["baseScore"]
        elif "cvssMetricV2" in self.json["metrics"]:
            return self.json["metrics"]["cvssMetricV2"][0]["cvssData"]["baseScore"]

        return None


    @property
    def cvss2_vector(self):  # noqa: ANN201
        if "cve" in self.json.keys():  # noqa: SIM118
            if "baseMetricV2" in self.json["impact"]:
                return self.json["impact"]["baseMetricV2"]["cvssV2"]["vectorString"]
        elif "cvssMetricV2" in self.json["metrics"]:
            return self.json["metrics"]["cvssMetricV2"][0]["cvssData"]["vectorString"]

        return None


    @property
    def cvss3_score(self):  # noqa: ANN201
        if "cve" in self.json.keys():  # noqa: SIM118
            if "baseMetricV3" in self.json["impact"]:
                return self.json["impact"]["baseMetricV3"]["cvssV3"]["baseScore"]
        elif "cvssMetricV31" in self.json["metrics"]:
            return self.json["metrics"]["cvssMetricV31"][0]["cvssData"]["baseScore"]
        elif "cvssMetricV30" in self.json["metrics"]:
            return self.json["metrics"]["cvssMetricV30"][0]["cvssData"]["baseScore"]

        return None

    @property
    def cvss3_vector(self):  # noqa: ANN201
        if "cve" in self.json.keys():  # noqa: SIM118
            if "baseMetricV3" in self.json["impact"]:
                return self.json["impact"]["baseMetricV3"]["cvssV3"]["vectorString"]
        elif "cvssMetricV31" in self.json["metrics"]:
            return self.json["metrics"]["cvssMetricV31"][0]["cvssData"]["vectorString"]
        elif "cvssMetricV30" in self.json["metrics"]:
            return self.json["metrics"]["cvssMetricV30"][0]["cvssData"]["vectorString"]

        return None

    @property
    def description(self) -> str:
        return self.json["descriptions"][0]["value"]
