from ulid import ULID
from datetime import datetime
from user.domain.user import User
from user.domain.repository.user_repo import IUserRepository
from user.infra.repository.user_repo import UserRepository

from fastapi import HTTPException

from dependency_injector.wiring import inject, Provide
from fastapi import Depends

# 유저 저장 및 중복 유저 검사 
class UserService:
    
    @inject  # 의존성 객체를 사용하는 함수에 주입받은 객체를 사용한다고 명시 
    def __init__(
        self,
        user_repo: IUserRepository,
    ):
        # 유저를 데이터베이스에 저장하는 저장소는 인프라 계층에 구현체가 있어야 한다. 
        # -> 외부의 서비스를 다루는 모듈은 그 수준이 낮기 때문이다. (데이터를 저장하기 위해 IUserRepository 사용 - 의존성 역전되어있음)
        self.user_repo = user_repo # IUserRepository = IUserRepository()

        # user_repo는 IUserRepository로 선언했지만, 실제 할당되는 객체는 UserRepository의 객체이다. 
        # 애플리케이션 계층이 인프라 계층에 직접 의존하고 있다. (클린 아키텍처의 대전제 위반) -> 이후 문제 해결 예정 
        self.ulid = ULID()

    def create_user(
            self, 
            name: str, 
            email: str, 
            password: str,
            memo: str | None = None
        ):

        _user = None

        try:
            _user = self.user_repo.find_by_email(email)

        except HTTPException as e:
            if e.status_code != 422:
                raise e
        
        # 같은 이메일로 가입된 유저가 있다면, 인프라 계층에서 422 에러를 일으킴
        if _user:
            raise HTTPException(status_code=422)

        now = datetime.now()
        user: User = User(  # 도메인 객체 생성 
            id=self.ulid.generate(),
            name=name,
            email=email,
            password=self.crypto.encrypt(password),  # 유저를 생성할 때 패스워드를 암호화해서 저장한다. 
            memo=memo,
            created_at=now,
            updated_at=now,
        )
        self.user_repo.save(user)  # 생성된 객체를 저장소로 전달해 저장

        return user


    def update_user(
            self,
            user_id: str,
            name: str | None = None,
            password: str | None = None,
    ):
        user = self.user_repo.find_by_id(user_id)

        # 이름 또는 패스워드 데이터가 전달되었을 때만 업데이트
        if name:
            user.name = name
        if password:
            user.password = self.crypto.encrypt(password)
        user.updated_at = datetime.now()

        self.user_repo.update(user)

        return user
    

    def get_users(self, page: int, items_per_page: int) -> tuple[int, list[User]]:
        users = self.user_repo.get_users(page, items_per_page)
        
        return users
    
    
    def delete_user(self, user_id: str):
        self.user_repo.delete(user_id)
        

