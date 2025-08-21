from __future__ import annotations

import re
import uuid
from pytz import timezone
from datetime import datetime
from typing import Optional

from pydantic import validator
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, func, text, Boolean, CheckConstraint, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import TIMESTAMP, CITEXT, BIGINT, UUID, TEXT as PG_TEXT


# ================= LANGUAGE ====================
class Language(SQLModel, table=True):
    __tablename__ = "languages"
    id: int = Field(primary_key=True)
    code: str = Field(max_length=250)
    name: str = Field(max_length=250)

class BaseModel(SQLModel):
    created_date: str = Field(default_factory=lambda: datetime.now(timezone('Asia/Tashkent')).strftime("%d:%m:%y"),
                              description="Yaratilgan vaqt")
    created_time: str = Field(default_factory=lambda: datetime.now(timezone('Asia/Tashkent')).strftime("%H:%M:%S"),
                              description="Yaratilgan vaqt")

    def to_dict(self) -> dict:
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


# ================= USER ====================
class User(BaseModel, table=True):
    """🔥 Eng xavfsiz foydalanuvchi modeli 🔥"""

    id: int = Field(default=None, primary_key=True)
    username: Optional[str] = Field(default=None, index=True)
    telegram_id: str = Field(unique=True, index=True)
    telegram_number: str = Field(max_length=12)
    telegram_name: str = Field(max_length=250)
    full_name: str = Field(default="", max_length=250)
    passport: str = Field(default="", max_length=32)
    faculty: str = Field(default="", max_length=100)
    jshir_id: str = Field(default="", max_length=13, nullable=True)
    status: bool = Field(default=False, nullable=False)
    language: str = Field(default="", max_length=32)


# ================= FACULTY ====================
class Faculty(BaseModel, table=True):
    __tablename__ = "faculties"
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=12)
    description: str = Field(default='')


# ================= ADMIN USER ====================
class AdminUser(BaseModel, table=True):
    __tablename__ = "admin_users"
    id: Optional[int] = Field(default=None, primary_key=True)
    username: Optional[str] = Field(default=None, index=True)
    telegram_id: str = Field(unique=True, index=True)
    telegram_number: str = Field(max_length=12)
    telegram_name: str = Field(max_length=250)
    name: str = Field(max_length=100, nullable=True)
    language: str = Field(default="", max_length=32)
