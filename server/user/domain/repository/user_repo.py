from abc import ABCMeta, abstractmethod
from user.domain.user import User

# 파이썬에서 제공하는 객체지향 인터페이스로 선언하기 위해 ABCMeta 클래스 이용
class IUserRepository(metaclass=ABCMeta):
    @abstractmethod  # 인터페이스의 구현체에서 구현할 함수를 abstractmethod로 선언
    def save(self, user: User):
        raise NotImplementedError  # 구현이 필요함을 기술 
        
    @abstractmethod
    def find_by_email(self, email: str) -> User:
        """
        저장소에서 이메일로 유저를 검색한다. 
        검색한 유저가 없을 경우 422 에러를 발생시킨다.
        (422 Error: 서버가 요청한 엔티티의 구문을 제대로 해석했지만, 명령을 수행할 수 없다는 뜻) 
        """
        raise NotImplementedError
    
    @abstractmethod
    def find_by_id(self, id: str) -> User:
        raise NotImplementedError
    
    @abstractmethod
    def update(self, user: User):
        raise NotImplementedError

    @abstractmethod
    def get_users(self, page: int, items_per_page: int) -> tuple[int, list[User]]:  # 함수 반환값 명시 -> mypy 같은 정적 분석기가 오류 검사시 도움됨
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, id: str):
        raise NotImplementedError