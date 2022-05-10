from pydantic import BaseSettings
from pydantic import SecretStr


class PostgresSettings(BaseSettings):
    host: str
    port: int
    dbname: str
    password: str
    user: str

    class Config:
        env_prefix = "POSTGRES_"


class URLSettings(BaseSettings):
    token: SecretStr
    api_url: str
    redirect_url: str
    lifetime_minutes: int
    domain: str

    class Config:
        env_prefix = "SHORT_URL_"


class SMTPSettings(BaseSettings):
    user: str
    password: SecretStr
    server: str
    port: int

    class Config:
        env_prefix = "SMTP_"
