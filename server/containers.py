from ulid import ULID
from dependency_injector import containers, providers

from user.application.send_welcome_email_task import SendWelcomeEmailTask
from user.application.email_service import EmailService
from user.application.user_service import UserService
from note.application.note_service import NoteService

from user.infra.repository.user_repo import UserRepository
from note.infra.repository.note_repo import NoteRepository

from utils.crypto import Crypto

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "user",
            "note",
        ],  # 의존성을 사용할 모듈 선언 
        # packages에 패키지 경로 기술하면 해당 패키지 위에 있는 모듈 모두 포함됨
        # 특정 모듈에만 제공하고 싶다면 modules=["user.application.user_service"]와 같이 등록할 수 있다. 
    )
    
    ulid = providers.Factory(ULID)
    crypto = providers.Factory(Crypto)  # Crypto 서비스 등록
    send_welcome_email_task = providers.Factory(SendWelcomeEmailTask)

    user_repo = providers.Factory(UserRepository)  # 의존성을 제공할 모듈을 팩토리에 등록한다. 
    email_service = providers.Factory(EmailService)
    
    user_service = providers.Factory(
        UserService, 
        user_repo=user_repo, 
        email_service=email_service,
        ulid=ulid,
        crypto=crypto, 
        send_welcome_email_task=send_welcome_email_task,
    )
    
    note_repo = providers.Factory(NoteRepository)
    note_service = providers.Factory(NoteService, note_repo=note_repo)

    
