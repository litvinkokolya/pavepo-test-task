from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Audio File Service Test Task"
    API_V1_STR: str = "/api/v1"

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_NAME: str
    POSTGRES_PORT: str = "5432"

    YANDEX_CLIENT_ID: str
    YANDEX_CLIENT_SECRET: str
    YANDEX_REDIRECT_URI: str = "http://127.0.0.1:8000/api/v1/users/yandex-auth" # Для удобства
    ALGORITHM: str

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 week

    AUDIO_FILES_DIR: str = "app/audio"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

DB_URL = (f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@"
            f"{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_NAME}")