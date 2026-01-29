from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str = "mariadb+pymysql://apiuser:apipassword@db:3306/apidb?charset=utf8mb4"
    SECRET_KEY: str = "THIS_IS_NOT_SECURE"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    PROJECT_NAME: str = "Location de propriétés"
    API_VERSION: str = "0.1.0"
    TOKEN_ENDPOINT: str = "http://auth:8080/token/issue"
    TOKEN_VALIDATE_ENDPOINT: str = "http://auth:8080/token/validate"

settings = Settings()

