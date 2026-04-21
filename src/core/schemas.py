from pydantic import BaseModel, ConfigDict, EmailStr, Field


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
    model_config = ConfigDict(from_attributes=True)


class UseDB(UserSchema):
    """User schema with ID for database storage"""

    id: int


class UserList(BaseModel):
    """Schema for a list of users"""

    users: list[UserPublic]


class Token(BaseModel):
    """Token schema for authentication responses"""

    access_token: str
    token_type: str


class FilterPage(BaseModel):
    """Schema for pagination and filtering"""

    offset: int = Field(0, ge=0)
    limit: int = Field(100, ge=1)
