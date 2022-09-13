import os

from daph_api.settings import settings


async def create_database() -> None:
    """Create a databse."""


async def drop_database() -> None:
    """Drop current database."""
    if settings.db_file.exists():
        os.remove(settings.db_file)
