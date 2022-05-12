from pydantic import BaseSettings
from pydantic import SecretStr
import environ

env_root = environ.Path(__file__) - 1
env = environ.Env()
env_file = str(env_root.path('.env'))
env.read_env(env_file)


class RabbitMQSettings(BaseSettings):
    default_user: str = 'guest'
    default_pass: SecretStr = 'guest'
    host: str = '127.0.0.1'

    class Config:
        env_prefix = "RABBITMQ_"


class LoggerSettings(BaseSettings):
    level: str = 'ERROR'

    class Config:
        env_prefix = "LOG_"


class SMTPSettings(BaseSettings):
    user: str
    password: SecretStr
    server: str
    port: int

    class Config:
        env_prefix = "SMTP_"


class PostgresSettings(BaseSettings):
    host: str = env('POSTGRES_HOST')
    port: int = env('POSTGRES_PORT')
    dbname: str = env('POSTGRES_DB')
    password: str = env('POSTGRES_PASSWORD')
    user: str = env('POSTGRES_USER')
