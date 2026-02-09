import sqlalchemy as sa

from src.core.config import settings

meta = sa.MetaData(naming_convention=settings.db.naming_convention)
