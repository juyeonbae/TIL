from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import get_settings

settings = get_settings()

# FastAPI는 객체 관계 매핑이 내장되어 있지 않다 -> SQLAlchemy 사용
# 객체 관계 매핑(ORM): 데이터베이스와 객체 지향 프로그래밍 언어 간의 데이터 변환을 도와주는 기술 

SQLALCHEMY_DATABASE_URL = (
    "mysql+mysqldb://"
    f"{settings.database_username}:{settings.database_password}"
    "@127.0.0.1/TIL"
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 클래스의 객체 생성 시, 데이터베이스 세션이 생성된다. (autocommit=True 설정 시, 롤백 불가능)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()