from datetime import datetime
from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class School(Base):
    __tablename__ = "schools"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(160))

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(160))
    email: Mapped[str] = mapped_column(String(180), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(30))
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"))
    active: Mapped[bool] = mapped_column(Boolean, default=True)

class Classroom(Base):
    __tablename__ = "classrooms"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"))
    teacher_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)

class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(160))
    classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id"))
    guardian_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)

class Lesson(Base):
    __tablename__ = "lessons"
    id: Mapped[int] = mapped_column(primary_key=True)
    classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id"))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    subject: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(Text)
    lesson_date: Mapped[datetime] = mapped_column(Date, default=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Event(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(primary_key=True)
    classroom_id: Mapped[int | None] = mapped_column(ForeignKey("classrooms.id"), nullable=True)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(180))
    description: Mapped[str] = mapped_column(Text, default="")
    event_type: Mapped[str] = mapped_column(String(30), default="atividade")
    due_date: Mapped[datetime] = mapped_column(Date)
    points: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Announcement(Base):
    __tablename__ = "announcements"
    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(180))
    body: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Notification(Base):
    __tablename__ = "notifications"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    message: Mapped[str] = mapped_column(String(255))
    read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
