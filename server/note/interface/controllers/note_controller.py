from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from dataclasses import asdict
from dependency_injector.wiring import inject, Provide
from datetime import datetime
from typing import Annotated

from common.auth import CurrentUser, get_current_user
from note.application.note_service import NoteService

from containers import Container


router = APIRouter(prefix="/notes")


class NoteResponse(BaseModel):
    id: str
    user_id: str
    title: str
    content: str
    memo_date: str
    tags: list[str]
    created_at: datetime
    updated_at: datetime


'''노트 생성'''
class CreateNoteBody(BaseModel):
    title: str = Field(min_length=1, max_length=64)
    content: str = Field(min_length=1)
    memo_date: str = Field(min_length=8, max_length=8)
    tags: list[str] | None = Field(default=None, min_length=1, max_length=32,)


@router.post("", status_code=201, response_model=NoteResponse)
@inject
def create_note(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    body: CreateNoteBody,
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    note = note_service.create_note(
        user_id=current_user.id,
        title=body.title,
        memo_date=body.memo_date,
        tag_names=body.tags if body.tags else [],
    )

    response = asdict(note)
    response.update({"tags": [tag.name for tag in note.tags]})

    return response


'''노트 목록 조회/노트 상세 조회'''
class GetNotesResponse(BaseModel):
    total_count: int
    page: int
    notes: list[NoteResponse]


@router.get("", response_model=GetNotesResponse)
@inject
def get_notes(
    page: int = 1,
    items_per_page: int = 10,
    current_user: CurrentUser = Depends(get_current_user),
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    total_count, notes = note_service.get_notes(
        user_id=current_user.id,
        page=page,
        items_per_page=items_per_page,
    )

    res_notes = []
    for note in notes:
        note_dict = asdict(note)
        note_dict.update({"tags": [tag.name for tag in note.tags]})  # 태그는 따로 매핑
        res_notes.append(note_dict)

    return {
        "total_count": total_count,
        "page": page,
        "notes": res_notes,
    }


'''노트 상세 조회'''
# 경로 매개변수로 조회할 노트 ID를 전달받는다. 
@router.get("/{id}", response_model=NoteResponse)
@inject
def get_note(
    id: str,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    note = note_service.get_note(
        user_id=current_user.id,
        id=id,
    )

    response = asdict(note)
    response.update({"tags": [tag.name for tag in note.tags]})

    return response


'''노트 업데이트'''
# 업데이트하고자 하는 노트의 ID를 경로 매개변수로 전달받는다. 
# 또, 업데이트할 항목을 본문으로 전달받는데, 이에 대한 파이단틱 모델을 따로 정의한다. 
class UpdateNoteBody(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=64)
    content: str | None = Field(default=None, min_length=1)
    memo_date: str | None = Field(default=None, min_length=8, max_length=8)
    tags: list[str] | None = Field(default=None)


@router.put("/{id}", response_model=NoteResponse)
@inject
def update_note(
    id: str,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    body: UpdateNoteBody,
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    note = note_service.update_note(
        user_id=current_user.id,
        id=id,
        title=body.title,
        cotent=body.content,
        memo_date=body.memo_date,
        tag_names=body.tags,
    )

    response = asdict(note)
    response.update({"tags": [tag.name for tag in note.tags]})

    return response


'''노트 삭제'''
@router.delete("/{id}", status_code=204)
@inject
def delete_note(
    id: str,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    note_service.delete_note(
        user_id=current_user.id,
        id=id,
    )


'''태그 이름으로 노트 검색'''
# API 사용 권한이 있는 유저와 노트 서비스와 페이징을 위한 쿼리 매개변수를 주입 받는다. 
@router.get("/tags/{tag_name}/notes", response_model=GetNotesResponse)  # 검색하고자 하는 태그 이름을 매개변수로 전달 받음 
@inject
def get_notes_by_tag(
    tag_name: str,
    page: int = 1,  # 같은 태그 이름을 가지는 노트가 많을 수 있기 때문에 페이징 적용 
    items_per_page: int = 10,
    current_user: CurrentUser = Depends(get_current_user),
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    total_count, notes = note_service.get_notes_by_tag(
        user_id=current_user.id,
        tag_name=tag_name,
        page=page,
        items_per_page=items_per_page,
    )

    res_notes = []  # tags를 응답에 맞는 형태로 변환
    for note in notes:
        note_dict = asdict(note)
        note_dict.update({"tags": [tag.name for tag in note.tags]})
        res_notes.append(note_dict)

    return {
        "total_count": total_count,
        "page": page,
        "notes": res_notes,
    }

