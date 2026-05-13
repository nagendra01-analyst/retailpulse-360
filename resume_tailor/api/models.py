"""
Pydantic models and SQLAlchemy ORM models for the Resume Tailor API.
"""
from __future__ import annotations

import enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import (
    Column,
    DateTime,
    Enum as SAEnum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import DeclarativeBase, relationship


# ---------------------------------------------------------------------------
# SQLAlchemy base
# ---------------------------------------------------------------------------

class Base(DeclarativeBase):
    pass


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class ResumeStyle(str, enum.Enum):
    PROFESSIONAL = "professional"
    MODERN = "modern"
    EXECUTIVE = "executive"
    MINIMAL_ATS = "minimal_ats"
    DATA_ANALYST = "data_analyst"
    BUSINESS_ANALYST = "business_analyst"
    AML_FRAUD_ANALYST = "aml_fraud_analyst"
    AI_DATA_SCIENCE = "ai_data_science"


class ExportFormat(str, enum.Enum):
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"


# ---------------------------------------------------------------------------
# ORM Models
# ---------------------------------------------------------------------------

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255))
    hashed_password = Column(String(255))
    google_sub = Column(String(255), unique=True, nullable=True)
    linkedin_sub = Column(String(255), unique=True, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    resumes = relationship("Resume", back_populates="owner", cascade="all, delete-orphan")
    jobs = relationship("JobDescription", back_populates="owner", cascade="all, delete-orphan")
    tailored = relationship("TailoredResume", back_populates="owner", cascade="all, delete-orphan")


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String(500))
    content_plain = Column(Text)
    encrypted_path = Column(String(1000), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    owner = relationship("User", back_populates="resumes")
    tailored_resumes = relationship("TailoredResume", back_populates="source_resume")


class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(500))
    company = Column(String(500))
    source_url = Column(String(2000), nullable=True)
    content = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    owner = relationship("User", back_populates="jobs")
    tailored_resumes = relationship("TailoredResume", back_populates="job")


class TailoredResume(Base):
    __tablename__ = "tailored_resumes"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    source_resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("job_descriptions.id"), nullable=False)
    style = Column(SAEnum(ResumeStyle), default=ResumeStyle.PROFESSIONAL)
    tailored_content = Column(Text)
    ats_score = Column(Float)
    missing_keywords = Column(Text)       # JSON list
    suggestions = Column(Text)            # JSON list
    created_at = Column(DateTime, server_default=func.now())

    owner = relationship("User", back_populates="tailored")
    source_resume = relationship("Resume", back_populates="tailored_resumes")
    job = relationship("JobDescription", back_populates="tailored_resumes")
    downloads = relationship("DownloadHistory", back_populates="tailored_resume", cascade="all, delete-orphan")


class DownloadHistory(Base):
    __tablename__ = "download_history"

    id = Column(Integer, primary_key=True, index=True)
    tailored_resume_id = Column(Integer, ForeignKey("tailored_resumes.id"), nullable=False)
    format = Column(SAEnum(ExportFormat))
    downloaded_at = Column(DateTime, server_default=func.now())

    tailored_resume = relationship("TailoredResume", back_populates="downloads")


# ---------------------------------------------------------------------------
# Pydantic schemas (request / response)
# ---------------------------------------------------------------------------

class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1)
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ResumeRead(BaseModel):
    id: int
    filename: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class JobDescriptionCreate(BaseModel):
    title: str = ""
    company: str = ""
    source_url: Optional[str] = None
    content: str = Field(..., min_length=50)


class JobDescriptionRead(BaseModel):
    id: int
    title: str
    company: str
    source_url: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class TailorRequest(BaseModel):
    resume_id: int
    job_id: int
    style: ResumeStyle = ResumeStyle.PROFESSIONAL


class ATSResult(BaseModel):
    ats_score: float = Field(..., ge=0, le=100, description="ATS match percentage 0–100")
    matched_keywords: list[str]
    missing_keywords: list[str]
    suggestions: list[str]


class TailoredResumeRead(BaseModel):
    id: int
    style: ResumeStyle
    tailored_content: str
    ats_score: float
    missing_keywords: list[str]
    suggestions: list[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class ExportRequest(BaseModel):
    tailored_resume_id: int
    format: ExportFormat = ExportFormat.PDF
    style: ResumeStyle = ResumeStyle.PROFESSIONAL
