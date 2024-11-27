from ulid import ULID
from datetime import datetime
from user.domain.user import User
from user.domain.repository.user_repo import IUserRepository
from user.infra.repository.user_repo import UserReopsitory

class UserService:
    def __init__(self):
        # 유저를 데이터베이스에 저장하는 저장소는 인프라 계층에 구현체가 있어야 한다. 
        # -> 외부의 서비스를 다루는 모듈은 그 수준이 낮기 때문이다. (데이터를 저장하기 위해 IUserRepository 사용 - 의존성 역전되어있음)
        self.user_repo: IUserRepository = UserRepository()

        # user_repo는 IUserRepository로 선언했지만, 실제 할당되는 객체는 UserRepository의 객체이다. 
        # 애플리케이션 계층이 인프라 계층에 직접 의존하고 있다. (클린 아키텍처의 대전제 위반) -> 이후 문제 해결 예정 
        self.ulid = ULID()

    def create_user(self, name: str, email: str, password: str):
        now = datetime.now()
        user: User = User(  # 도메인 객체 생성 
            id=self.ulid.generate(),
            name=nmae,
            email=email,
            password=password,
            created_at=now,
            updated_at=now,
        )
        self.user_repo.save(user)  # 생성된 객체를 저장소로 전달해 저장 

