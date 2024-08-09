from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool

    class Config:
        from_attributes = True


class UserRegistrationSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    is_active: bool

    class Config:
        from_attributes = True


class UserUpdateSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class UserPartialUpdateSchema(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
