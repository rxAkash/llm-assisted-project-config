from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    snowflake_account: str = ""
    snowflake_user: str = ""
    snowflake_password: str = ""
    snowflake_warehouse: str = ""
    snowflake_database: str = ""
    postgres_dsn: str = "postgresql://app:app@localhost:5432/app"
