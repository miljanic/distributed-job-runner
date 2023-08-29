from typing import Optional

from djb_api.application.db import db
from djb_api.domain.auth.dto import User, UserCreate
from djb_api.domain.auth.exceptions import UsernameTaken
from psycopg.errors import UniqueViolation
from psycopg.rows import class_row


class UserRepository:
    async def get_by_username(self, username: str) -> Optional[User]:
        conn = await db.get_conn()
        async with conn.cursor(row_factory=class_row(User)) as cur:
            await cur.execute(
                "SELECT id, username, hashed_password, api_key FROM users WHERE username = %s",
                (username,),
            )
            return await cur.fetchone()

    async def save_user(self, data: UserCreate) -> None:
        try:
            await db.execute(
                "INSERT INTO users (username, hashed_password, api_key) VALUES (%s, %s, %s)",
                (data.username, data.hashed_password, data.api_key),
            )
        except UniqueViolation:
            raise UsernameTaken()
