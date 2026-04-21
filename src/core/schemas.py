from pydantic import BaseModel, ConfigDict, EmailStr, Field

from core.models import TodoState


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


class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodoState


class TodoPublic(TodoSchema):
    id: int


class TodoList(BaseModel):
    todos: list[TodoPublic]


class FilterTodo(FilterPage):
    title: str | None = Field(None, min_length=3, max_length=20)
    description: str | None = Field(None, min_length=3, max_length=20)
    state: TodoState | None = None


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None
