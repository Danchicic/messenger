import logging
from typing import Optional

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.auth import User
from . import schemas

logger = logging.getLogger(__name__)


class UserService:
    @staticmethod
    async def get_user(user_info: str, session: AsyncSession, by: str = "id") -> Optional[User]:
        if by == "id":
            query = select(User).where(User.id == int(user_info))
        else:
            logger.info(f"ph: {user_info}, {type(user_info)}")

            query = select(User).where(User.phone_number == user_info)
        user = await session.execute(query)
        return user.scalar()

    @staticmethod
    async def create_user(user: schemas.User, session: AsyncSession) -> User:
        query = insert(User).values({"phone_number": str(user.phone_number.phone_number)}).returning(User)
        user = await session.execute(query)
        return user.scalar()
