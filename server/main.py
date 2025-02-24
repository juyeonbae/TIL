import uvicorn
from fastapi import FastAPI
from user.interface.controllers.user_controller import router as user_routers
from note.interface.controllers.note_controller import router as note_routers

from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from containers import Container
from middlewares import create_middlewares

app = FastAPI()
app.container = Container()
app.container.wire(modules=["user.interface.controllers.user_controller"])  # 추가된 부분

create_middlewares(app)

app.include_router(user_routers)
app.include_router(note_routers)

# FastAPI는 400 에러를 422 에러로 처리함 -> 400 에러로 처리하는 방법 
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=400,  # 응답 코드를 400으로 변경
        content=exc.errors(),  # 예외 객체의 에러를 응답의 본문으로 전달
    )

@app.get("/")
def hello():
    return {"Hello": "FastAPI"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True)