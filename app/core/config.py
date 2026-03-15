from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "To-Do API"
    debug: bool = False
    database_url: str = "sqlite:///./todo.db"


settings = Settings()
