import logging
from sqlalchemy import ScalarResult, delete, select, insert, update

from typing import Callable, List
from pydantic import UUID3
from sqlalchemy.exc import DBAPIError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine.result import ChunkedIteratorResult

from bot.db.models import Advertisement, User

logger = logging.getLogger(__name__)


class DbRepository:
    __slots__ = ('session_factory',)

    def __init__(self, session_factory: sessionmaker[AsyncSession]):
        self._session_factory = session_factory
        
