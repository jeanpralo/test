import logging

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Query
from sqlalchemy import desc


Base = declarative_base()

logger = logging.getLogger(__name__)


class BaseModel(Base):
    __abstract__ = True

    @classmethod
    def get_column(cls, column_name: str):
        if hasattr(cls, column_name):
            return getattr(cls, column_name)
        return None

    @classmethod
    def sort_job_query(cls, query: Query, sort: str):
        if sort:
            _args = sort.split(":")  # column_name:direction
            if len(_args) == 2 and _args[1].lower() in ("asc", "desc"):
                column_obj = cls.get_column(_args[0])
                if column_obj:
                    logger.debug(f'Ordering jobs by {_args}')
                    if _args[1].lower() == 'desc':
                        return query.order_by(desc(column_obj))
                    else:
                        return query.order_by(column_obj)

        return query

    @classmethod
    def filter_job_query(cls, query: Query, filters: dict):
        if not filters:
            return query

        for column, value in filters.items():
            column_obj = cls.get_column(column)
            if column_obj:
                logger.debug(f'Filter {cls.__name__} query with {column} = {value}')
                query = query.filter(column_obj == value)
            else:
                logger.debug(f'Skipping unknown column: {column}')

        return query
