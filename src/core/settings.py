from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

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
