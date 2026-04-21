from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )

    DATABASE_URL: str = 'sqlite+aiosqlite:///database.db'
    SECRET_KEY: str = 'your-secret-key'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @field_validator('DATABASE_URL', mode='before')
    @classmethod
    def default_database_url(cls, value):
        if isinstance(value, str) and not value:
            return 'sqlite+aiosqlite:///database.db'
        return value

    @field_validator('SECRET_KEY', mode='before')
    @classmethod
    def default_secret_key(cls, value):
        if isinstance(value, str) and not value:
            return 'your-secret-key'
        return value

    @field_validator('ALGORITHM', mode='before')
    @classmethod
    def default_algorithm(cls, value):
        if isinstance(value, str) and not value:
            return 'HS256'
        return value

    @field_validator('ACCESS_TOKEN_EXPIRE_MINUTES', mode='before')
    @classmethod
    def default_access_token_expire_minutes(cls, value):
        if isinstance(value, str) and not value:
            return 30
        return value

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        """Return an async SQLAlchemy database URL."""
        if self.DATABASE_URL.startswith('postgresql+psycopg://'):
            return self.DATABASE_URL.replace(
                'postgresql+psycopg://', 'postgresql+psycopg_async://', 1
            )
        if self.DATABASE_URL.startswith('sqlite:///'):
            return self.DATABASE_URL.replace(
                'sqlite:///', 'sqlite+aiosqlite:///', 1
            )
        return self.DATABASE_URL

    @property
    def SYNC_DATABASE_URL(self) -> str:
        """Return a sync SQLAlchemy database URL."""
        if self.DATABASE_URL.startswith('postgresql+asyncpg://'):
            return self.DATABASE_URL.replace(
                'postgresql+asyncpg://', 'postgresql+psycopg://', 1
            )
        if self.DATABASE_URL.startswith('postgresql+psycopg_async://'):
            return self.DATABASE_URL.replace(
                'postgresql+psycopg_async://', 'postgresql+psycopg://', 1
            )
        if self.DATABASE_URL.startswith('sqlite+aiosqlite:///'):
            return self.DATABASE_URL.replace(
                'sqlite+aiosqlite:///', 'sqlite:///', 1
            )
        return self.DATABASE_URL
