from abc import ABCMeta, abstractmethod
from note.domain.note import Note


# 노트를 데이터베이스에 저장하고 다루는 저장소의 인터페이스 정의 
class INoteRepository(metaclass=ABCMeta):
    @abstractmethod  # 반드시 구현해야하는 메서드라고 python에 알려주는 것
    def get_notes(
        self,
        user_id: str,
        page: int,
        items_per_page: int,
    ) -> tuple[int, list[Note]]:
        raise NotImplementedError
    
    @abstractmethod
    def fine_by_id(self, user_id: str, id: str) -> Note:
        raise NotImplementedError
    
    @abstractmethod
    def save(self, user_id: str, note: Note) -> Note:
        raise NotImplementedError
    
    @abstractmethod
    def update(self, user_id: str, note: Note) -> Note:
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, user_id: str, id: str):  
        raise NotImplementedError
    
    @abstractmethod
    def delete_tags(self, user_id: str, id: str): # 노트 수정 시 태그를 수정하지 않고 모두 지웠다가 다시 추가하기 위함
        raise NotImplementedError

    @abstractmethod
    def get_notes_by_tag_name(
        self, 
        user_id: str,
        tag_name: str,
        page: int, 
        items_per_page: int,
    ) -> tuple[int, list[Note]]:
        raise NotImplementedError
    
