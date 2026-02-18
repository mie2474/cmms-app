from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    APP_NAME: str = "CMMS Backend"
    APP_ENV: str = "dev"

    # Database
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # Okta
    OKTA_DOMAIN: str
    OKTA_CLIENT_ID: str
    OKTA_CLIENT_SECRET: str
    OKTA_REDIRECT_URI: str
    OKTA_ISSUER: str
    OKTA_AUDIENCE: str

    class Config:
        env_file = ".env"


settings = Settings()
