from pydantic_settings import SettingsConfigDict, BaseSettings

class Config(BaseSettings):
    DB_PATH: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )
    
setting = Config()
print(setting.DB_PATH)