from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.src.users.models import User
from backend.src.users.schemas import (
    UserPartialUpdateSchema,
    UserRegistrationSchema,
    UserUpdateSchema,
)


async def get(*, db_session: AsyncSession, user_id: int) -> User | None:
    result = await db_session.execute(select(User).filter(User.id == user_id))
    return result.scalars().one_or_none()


async def get_by_email(*, db_session: AsyncSession, email: str) -> User | None:
    result = await db_session.execute(select(User).filter(User.email == email))
    return result.scalars().one_or_none()


async def create(*, db_session: AsyncSession, data: UserRegistrationSchema) -> User:
    user = User(
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
        password=data.password,
        is_active=data.is_active,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


async def update(
    *, db_session: AsyncSession, user: User, data: UserUpdateSchema | UserPartialUpdateSchema
) -> User:
    update_data = data.model_dump(exclude_none=True)
    if not update_data:
        return user

    for field in update_data:
        setattr(user, field, update_data[field])

    await db_session.commit()
    await db_session.refresh(user)

    return user
