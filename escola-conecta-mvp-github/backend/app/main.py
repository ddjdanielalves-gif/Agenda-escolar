import os
from datetime import date, datetime, timedelta, timezone
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from .models import Announcement, Classroom, Event, Lesson, Notification, School, Student, User
from .schemas import AnnouncementIn, EventIn, LessonIn, Login, Token

SECRET_KEY = os.getenv("SECRET_KEY", "development-only-change-me")
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
app = FastAPI(title="Escola Conecta API", version="0.1.0")
origins = [x.strip() for x in os.getenv("FRONTEND_ORIGIN", "http://localhost:5173").split(",")]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

def create_token(user: User):
    return jwt.encode({"sub": str(user.id), "role": user.role, "exp": datetime.now(timezone.utc) + timedelta(hours=12)}, SECRET_KEY, algorithm=ALGORITHM)
def current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try: user_id = int(jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])["sub"])
    except (JWTError, KeyError, ValueError): raise HTTPException(status_code=401, detail="Sessão inválida")
    user = db.get(User, user_id)
    if not user or not user.active: raise HTTPException(status_code=401, detail="Usuário indisponível")
    return user
def require(*roles):
    def guard(user: User = Depends(current_user)):
        if user.role not in roles: raise HTTPException(status_code=403, detail="Sem permissão")
        return user
    return guard
def payload(model):
    return {c.name: getattr(model, c.name) for c in model.__table__.columns}

@app.on_event("startup")
def startup():
    Base.metadata.create_all(engine)
    with next(get_db()) as db:
        if db.scalar(select(User.id).limit(1)): return
        school = School(name="Escola Exemplo"); db.add(school); db.flush()
        users = [User(name="Ana Professora", email="professor@escola.com", password_hash=pwd_context.hash("123456"), role="teacher", school_id=school.id), User(name="Maria Responsável", email="responsavel@escola.com", password_hash=pwd_context.hash("123456"), role="guardian", school_id=school.id), User(name="Carlos Administrador", email="admin@escola.com", password_hash=pwd_context.hash("123456"), role="admin", school_id=school.id)]
        db.add_all(users); db.flush()
        turma = Classroom(name="7º Ano A", school_id=school.id, teacher_id=users[0].id); db.add(turma); db.flush()
        db.add(Student(name="João Silva", classroom_id=turma.id, guardian_id=users[1].id))
        db.add(Announcement(school_id=school.id, author_id=users[2].id, title="Boas-vindas", body="Bem-vindos à plataforma Escola Conecta."))
        db.add(Event(classroom_id=turma.id, created_by=users[0].id, title="Trabalho de Matemática", description="Equações do 1º grau", event_type="trabalho", due_date=date.today()+timedelta(days=7), points=2))
        db.commit()

@app.get("/health")
def health(): return {"status": "ok"}
@app.post("/auth/login", response_model=Token)
def login(data: Login, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == data.email))
    if not user or not pwd_context.verify(data.password, user.password_hash): raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="E-mail ou senha inválidos")
    return {"access_token": create_token(user), "user": {"id":user.id,"name":user.name,"role":user.role,"school_id":user.school_id}}
@app.get("/me")
def me(user: User = Depends(current_user)): return {"id":user.id,"name":user.name,"email":user.email,"role":user.role}
@app.get("/dashboard")
def dashboard(user: User = Depends(current_user), db: Session = Depends(get_db)):
    events = db.scalars(select(Event).join(Classroom, Event.classroom_id == Classroom.id, isouter=True).where((Classroom.school_id == user.school_id) | (Event.classroom_id == None)).order_by(Event.due_date).limit(6)).all()
    announcements = db.scalars(select(Announcement).where(Announcement.school_id == user.school_id).order_by(Announcement.created_at.desc()).limit(5)).all()
    return {"events":[payload(x) for x in events], "announcements":[payload(x) for x in announcements], "stats":{"events":len(events),"classes":db.scalar(select(Classroom).where(Classroom.school_id==user.school_id).count()) if False else len(db.scalars(select(Classroom).where(Classroom.school_id==user.school_id)).all())}}
@app.get("/classrooms")
def classrooms(user: User = Depends(current_user), db: Session = Depends(get_db)):
    return [payload(x) for x in db.scalars(select(Classroom).where(Classroom.school_id == user.school_id)).all()]
@app.get("/events")
def events(user: User = Depends(current_user), db: Session = Depends(get_db)):
    return [payload(x) for x in db.scalars(select(Event).order_by(Event.due_date)).all()]
@app.post("/events")
def add_event(data: EventIn, user: User = Depends(require("teacher", "admin")), db: Session = Depends(get_db)):
    event = Event(**data.model_dump(), created_by=user.id); db.add(event); db.flush()
    db.add(Notification(user_id=user.id, message=f"Atividade '{event.title}' agendada para {event.due_date.strftime('%d/%m')}.")); db.commit()
    return payload(event)
@app.get("/lessons")
def lessons(user: User = Depends(current_user), db: Session = Depends(get_db)):
    return [payload(x) for x in db.scalars(select(Lesson).order_by(Lesson.lesson_date.desc())).all()]
@app.post("/lessons")
def add_lesson(data: LessonIn, user: User = Depends(require("teacher", "admin")), db: Session = Depends(get_db)):
    lesson = Lesson(**data.model_dump(), teacher_id=user.id); db.add(lesson); db.commit(); db.refresh(lesson); return payload(lesson)
@app.get("/announcements")
def announcements(user: User = Depends(current_user), db: Session = Depends(get_db)):
    return [payload(x) for x in db.scalars(select(Announcement).where(Announcement.school_id == user.school_id).order_by(Announcement.created_at.desc())).all()]
@app.post("/announcements")
def add_announcement(data: AnnouncementIn, user: User = Depends(require("admin", "teacher")), db: Session = Depends(get_db)):
    item = Announcement(**data.model_dump(), school_id=user.school_id, author_id=user.id); db.add(item); db.commit(); db.refresh(item); return payload(item)
