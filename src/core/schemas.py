from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    """Message schema for API responses"""

    message: str


class UserSchema(BaseModel):
    """User creation schema"""

    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    """User public schema"""

    id: int
    username: str
    email: EmailStr


class UseDB(UserSchema):
    """User schema with ID for database storage"""

    id: int


class UserList(BaseModel):
    """Schema for a list of users"""

    users: list[UserPublic]
