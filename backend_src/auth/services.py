from typing import Optional

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.auth import User
from . import schemas


class UserService:
    @staticmethod
    async def get_user(user_info: str, session: AsyncSession, by: str = "id") -> Optional[User]:
        if by == "id":
            query = select(User).where(User.id == int(user_info))
        else:
            query = select(User).where(User.phone_number == int(user_info))
        user = await session.execute(query)
        return user.one_or_none()

    @staticmethod
    async def create_user(user: schemas.User, session: AsyncSession) -> User:
        query = insert(User).values({"phone_number": user.phone_number.phone_number}).returning(User)
        user = await session.execute(query)
        return user.scalar()
