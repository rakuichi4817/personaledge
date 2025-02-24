import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """接続先情報の基本設定を取得する

    Notes:
        .envファイルから設定を読み込む
    """

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    )

    aoai_endpoint: str = ""
    aoai_api_version: str = ""
    aoai_api_key: str = ""
    deployment_name: str = ""


def get_settings() -> Settings:
    return Settings()


settings = get_settings()
