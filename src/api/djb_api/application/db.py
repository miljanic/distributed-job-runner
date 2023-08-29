from typing import Any, Optional

from djb_api.config import config
from fastapi import Request, Response
from psycopg import AsyncConnection, AsyncCursor
from psycopg.abc import Params, Query
from psycopg.rows import TupleRow

DATABASE_URL = config.db.DATABASE_URI
LOG_LEVEL = config.db.LOG_LEVEL


class Database:
    _conn: Optional[AsyncConnection[Any]] = None

    async def get_conn(self) -> AsyncConnection[Any]:
        if self._conn is None:
            self._conn = await AsyncConnection.connect(DATABASE_URL, autocommit=True)

        return self._conn

    async def execute(
        self,
        query: Query,
        params: Optional[Params] = None,
        *,
        prepare: Optional[bool] = None,
        binary: bool = False,
    ) -> AsyncCursor[TupleRow]:
        return await (await self.get_conn()).execute(
            query,
            params,
            prepare=prepare,
            binary=binary,
        )

    async def close(self) -> None:
        await (await self.get_conn()).close()

    async def exception_handler(self, req: Request, exception: Exception) -> Response:
        await (await self.get_conn()).rollback()
        await self.close()
        raise exception


db = Database()
