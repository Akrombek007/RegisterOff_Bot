from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from pytz import timezone


# ================= LANGUAGE ====================
class Language(SQLModel, table=True):
    __tablename__ = "languages"
    id: int = Field(primary_key=True)
    code: str = Field(max_length=250)
    name: str = Field(max_length=250)


class BaseModel(SQLModel):
    id: int = Field(default=None, primary_key=True, index=True)
    created_date: str = Field(default_factory=lambda: datetime.now(timezone('Asia/Tashkent')).strftime("%d:%m:%y"),
                              description="Yaratilgan vaqt")
    created_time: str = Field(default_factory=lambda: datetime.now(timezone('Asia/Tashkent')).strftime("%H:%M:%S"),
                              description="Yaratilgan vaqt")

    def to_dict(self) -> dict:
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


# ================= USER ====================
class User(BaseModel, table=True):
    """🔥 Eng xavfsiz foydalanuvchi modeli 🔥"""
    username: Optional[str] = Field(default=None, index=True)
    telegram_id: str = Field(unique=True, index=True)
    telegram_number: str = Field(max_length=12)
    telegram_name: str = Field(max_length=250)
    full_name: str = Field(default="", max_length=250)
    passport: str = Field(default="", max_length=32)
    faculty: str = Field(default="", max_length=100)
    group: str = Field(default="", max_length=100)
    jshir_id: str = Field(default="", max_length=13, nullable=True)
    status: bool = Field(default=False, nullable=False)
    language: str = Field(default="", max_length=32)
    # support_requests: list["SupportRequest"] = Relationship(back_populates="user")


# ================= FACULTY ====================
class Faculty(BaseModel, table=True):
    __tablename__ = "faculties"
    name: str = Field(max_length=12)
    description: str = Field(default='')


# ================= ADMIN USER ====================
class AdminUser(BaseModel, table=True):
    __tablename__ = "admin_users"
    username: Optional[str] = Field(default=None, index=True)
    telegram_id: str = Field(unique=True, index=True)
    telegram_number: str = Field(max_length=12)
    telegram_name: str = Field(max_length=250)
    name: str = Field(max_length=100, nullable=True)
    faculty: str = Field(default="", max_length=100)
    language: str = Field(default="", max_length=32)
    # admin_responses: list["SupportRequest"] = Relationship(back_populates="admin")


class SupportRequest(BaseModel, table=True):
    __tablename__ = "support_requests"

    user_id: str = Field(default='')
    admin_id: str = Field(default='')

    question_text: str = Field(default='')
    answer_text: str = Field(default='')
    message_id: str = Field(default='')

    started_date: str = Field(default_factory=lambda: datetime.now(timezone('Asia/Tashkent')).strftime("%d:%m:%y"),
                              description="Yaratilgan vaqt")
    started_time: str = Field(default_factory=lambda: datetime.now(timezone('Asia/Tashkent')).strftime("%H:%M:%S"),
                              description="Yaratilgan vaqt")
    end_date: str = Field(default='')
    end_time: str = Field(default='')

    feedback: bool = Field(default=False)

    # user: Mapped[Optional["User"]] = Relationship(back_populates="support_requests")
    # admin: Mapped[Optional["AdminUser"]] = Relationship(back_populates="admin_responses")