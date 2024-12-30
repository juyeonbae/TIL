from fastapi import APIRouter, Depends
from typing import Annotated
from pydantic import BaseModel 
from containers import Container
from dependency_injector.wiring import inject, Provide

from user.application.user_service import UserService

router = APIRouter(prefix="/users")  # APIRouter 객체 생성 - API 경로에 /users로 시작하도록 함

# 회원 가입 라우터로 전달된 외부의 요청에 포함돼 있는 본문을 검사함
class CreateUserBody(BaseModel):
    name: str
    email: str
    password: str

# /users라는 경로로 POST 요청을 받을 수 있다.
# 유저 리소스 생성이 성공했을 때 응답의 HTTP 상태 코드 201 (요청이 성공적으로 처리되었으며, 자원이 생성되었음을 나타냄)
# 응답이 반환되기 이전에 새로운 리소스가 생성되며, 응답 메시지 본문에 새로 만드러진 리소스 또는 리소스에 대한 설명과 링크를 메시지 본문에 넣어 반환
# 그 위치는 요청 URL 또는 Location(en-US) 헤더 값의 URL 

# API의 진입점을 나타내는 라우터 함수: (경로 수행 함수, 엔드포인트 함수, 라우터 함수)라고 함
@router.post("", status_code=201)   
@inject 
# 유저 생성 유스 케이스 호출 / 인터페이스 계층은 애플리케이션 계층에 의존해도 된다. 
def create_user(
    user: CreateUserBody,
    user_service: UserService = Depends(Provide[Container.user_service]),  # dependency_injector로 주입 받음
    # user_service: UserService = Depends(Provide["user_service"]), 
    # 리터럴 문자열로도 가능 -> 컨테이너에 등록된 모듈이 서로를 주입해야 하는 경우 순환 참조가 발생하기 때문이다. 
    # 그러나 실질적으로는 안 사라짐 (빌드 에러만 해결함) SW 구조적으로 좋지 않다. 
    # 실질적 해결 방안: 순환 참조가 일어나는 부분을 다른 모듈로 분리하고, 해당 모듈을 함께 사용하는 것이 좋다. 
):
    # user_service = UserService()
    created_user = user_service.create_user(
        name=user.name,
        email=user.email,
        password=user.password
    )
    return created_user  # 유스 케이스 함수의 응답: 새로 생성된 유저 도메인 객체 