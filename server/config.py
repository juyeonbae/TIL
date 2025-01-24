from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    database_username: str
    database_password: str
    jwt_secret: str

    sender_email: str
    email_password: str

    celery_broker_url: str
    celery_backend_url: str

@lru_cache  # 페이지 교체 알고리즘(LRU) - 인수에 따라 동작이 달라진다면 성능 향상 
def get_settings():  # 환경변수 파이단틱 모델의 객체를 생성한다. - 다른 모듈은 이 함수를 호출해서 환경변수를 읽을 수 있다. 
    return Settings()