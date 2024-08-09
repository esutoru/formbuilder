import typer as typer
from email_validator import EmailNotValidError, validate_email
from rich import print as rich_print
from syncer import sync

from backend.src.auth.security import get_password_hash
from backend.src.dashboard import services as dashboard_service
from backend.src.dashboard.schemas import DashboardCreateSchema
from backend.src.database.core import async_session, engine
from backend.src.users import services as user_service
from backend.src.users.schemas import UserRegistrationSchema, UserSchema

app = typer.Typer()


@sync
async def _validate_email(value: str) -> str:
    try:
        email = validate_email(value).normalized
    except EmailNotValidError as exc:
        raise typer.BadParameter(str(exc))

    try:
        async with async_session() as session:
            if await user_service.get_by_email(db_session=session, email=email):
                raise typer.BadParameter(f"User with email {email} already exists")
    finally:
        await engine.dispose()

    return email


def _validate_password(value: str) -> str:
    if len(value) < 8:
        raise typer.BadParameter("Your password must contain at least 8 characters")
    return value


@app.command("create")
@sync
async def create(
    email: str = typer.Option(..., prompt=True, callback=_validate_email),
    first_name: str = typer.Option(..., prompt=True, min=1, max=20),
    last_name: str = typer.Option(..., prompt=True, min=1, max=20),
    password: str = typer.Option(
        ..., prompt=True, confirmation_prompt=True, hide_input=True, callback=_validate_password
    ),
) -> None:
    """Create new user."""

    data = UserRegistrationSchema(
        email=email,
        password=get_password_hash(password),
        is_active=True,
        first_name=first_name,
        last_name=last_name,
    )
    async with async_session() as session:
        user = await user_service.create(db_session=session, data=data)
        if user:
            await dashboard_service.create_dashboard(
                db_session=session,
                user_id=user.id,
                data=DashboardCreateSchema(name="Default Dashboard"),
            )
            await session.commit()
            await session.refresh(user)

    rich_print("New user successfully created! :tada:")
    rich_print(UserSchema.model_validate(user).model_dump())
