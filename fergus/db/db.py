import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


class Db(object):
    def __init__(self):
        self._engine = create_engine("sqlite:///database.db")
        self._session_maker = sessionmaker(bind=self._engine, expire_on_commit=True)

    def __enter__(self):
        self._session = self._session_maker()
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()

    def close(self):
        self._engine.dispose()
