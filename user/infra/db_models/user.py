from datetime import datetime
from sqlalchemy import String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

# datebase 모듈에서 declarative_base 함수에 의해 생성된 Base 클래스를 상속 받는다. 
# declarative_base 함수: 선언형 클래스를 정의하기 위한 기본 클래스 생성
# 생성된 기본 클래스는 메타클래스를 얻는다. > 이는 적합한 Table 객체를 생성하고, 
# 클래스 내에서 선언된 정보와 클래스의 하위 클래스로부터 제공된 정보를 기반으로 적절한 매퍼를 생성한다. 
# (즉, 테이블을 생성하고 다룰 수 있는 클래스를 생성한다.)
class User(Base):  
    __tablename__ = "User"  # 테이블 이름 지정 
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)  # UUID 또는 ULID 같은 문자열 사용할거라 String 지정 
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    email: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)  # unique: 유일한 값
    password: Mapped[str] = mapped_column(String(64), nullable=False)
    memo: Mapped[str] = mapped_column(Text, nullable=True)  # 메모는 없을 수도 있으므로 Null 허용 
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

'''
Alembic을 이용해 테이블 생성
* Alebic: SQLAlchemy와 함께 사용되는 데이터베이스 마이그레이션 도구 
(테이블 생성, 수정, 삭제 등, 마이그레이션 파일 생성해 스키마의 버전 관리 가능)

1. Alembic 설치
>> poetry add sqlalchemy mysqlclient alembic

2. Alembic 초기화 수행
>> alembic init migrations 
'''