from dependency_injector import containers, providers
from user.infra.repository.user_repo import UserRepository
from user.application.user_service import UserService

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["user"],  # 의존성을 사용할 모듈 선언 
        # packages에 패키지 경로 기술하면 해당 패키지 위에 있는 모듈 모두 포함됨
        # 특정 모듈에만 제공하고 싶다면 modules=["user.application.user_service"]와 같이 등록할 수 있다. 
    )
    
    user_repo = providers.Factory(UserRepository)  # 의존성을 제공할 모듈을 팩토리에 등록한다. 
    user_service = providers.Factory(UserService, user_repo=user_repo)
    