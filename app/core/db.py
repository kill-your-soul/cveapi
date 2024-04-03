from app.core.config import settings
# from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import create_async_engine


engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI))
