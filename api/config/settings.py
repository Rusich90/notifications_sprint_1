from pydantic import BaseSettings
from pydantic import SecretStr


class RabbitMQSettings(BaseSettings):
    default_user: str = 'guest'
    default_pass: SecretStr = 'guest'
    host: str = 'localhost'

    class Config:
        env_prefix = "RABBITMQ_"


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
