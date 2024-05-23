from celery import Celery
from celery.schedules import crontab
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore",
    )
    NVD_API_URL: str
    CVE_API_URL: str
    BDU_XLSX_URL: str
    BROKER: str
    MITRE_CWE_URL: str
    REPO_URL: str


settings = Settings()
celery = Celery("update", broker=settings.BROKER)

celery.conf.beat_schedule = {
    "run-everyday": {
        "task": "update.update",
        "schedule": crontab(minute=00, hour=9),
    },
}
celery.conf.timezone = "Europe/Moscow"
