from pydantic import computed_field
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

    @computed_field
    @property
    def ASYNC_DATABASE_URL(self) -> str:
        """Returns a SQLAlchemy async database URL."""
        if self.DATABASE_URL.startswith('sqlite:///'):
            return self.DATABASE_URL.replace(
                'sqlite:///', 'sqlite+aiosqlite:///', 1
            )
        return self.DATABASE_URL

    @computed_field
    @property
    def SYNC_DATABASE_URL(self) -> str:
        """Returns a SQLAlchemy sync database URL."""
        if self.DATABASE_URL.startswith('sqlite+aiosqlite:///'):
            return self.DATABASE_URL.replace(
                'sqlite+aiosqlite:///', 'sqlite:///', 1
            )
        return self.DATABASE_URL
