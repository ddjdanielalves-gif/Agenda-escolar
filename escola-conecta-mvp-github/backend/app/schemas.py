from datetime import date, datetime
from pydantic import BaseModel, EmailStr

class Login(BaseModel): email: EmailStr; password: str
class Token(BaseModel): access_token: str; token_type: str = "bearer"; user: dict
class LessonIn(BaseModel): classroom_id: int; subject: str; content: str; lesson_date: date
class EventIn(BaseModel): classroom_id: int | None = None; title: str; description: str = ""; event_type: str = "atividade"; due_date: date; points: float | None = None
class AnnouncementIn(BaseModel): title: str; body: str
