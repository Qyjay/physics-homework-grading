"""
数据库配置和模型定义
SQLAlchemy Database Configuration
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# 数据库 URL（SQLite 用于开发环境）
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./physics_homework.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============== User Model ==============

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="teacher")  # teacher / student
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关联
    classes = relationship("Class", back_populates="teacher")
    gradings = relationship("Grading", back_populates="user")
    standard_answers = relationship("StandardAnswer", back_populates="creator")


# ============== Image Model ==============

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(String(50), unique=True, index=True, nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    size = Column(Integer)  # bytes
    width = Column(Integer)
    height = Column(Integer)
    student_name = Column(String(100))
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    # 关联
    gradings = relationship("Grading", back_populates="image")


# ============== Standard Answer Model ==============

class StandardAnswer(Base):
    __tablename__ = "standard_answers"

    id = Column(Integer, primary_key=True, index=True)
    answer_id = Column(String(50), unique=True, index=True, nullable=False)
    question_title = Column(String(255), nullable=False)
    subject = Column(String(50), default="physics")
    grade = Column(String(50), default="high_school_1")
    chapter = Column(String(100))
    steps = Column(JSON)  # [{"order": 1, "description": "...", "content": "...", "formula": "...", "score": 3.0}]
    total_score = Column(Float, default=10.0)
    tags = Column(JSON)  # ["力学", "牛顿定律"]
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联
    creator = relationship("User", back_populates="standard_answers")
    gradings = relationship("Grading", back_populates="standard_answer")


# ============== Grading Model ==============

class Grading(Base):
    __tablename__ = "gradings"

    id = Column(Integer, primary_key=True, index=True)
    grading_id = Column(String(50), unique=True, index=True, nullable=False)
    image_id = Column(Integer, ForeignKey("images.id"))
    standard_answer_id = Column(Integer, ForeignKey("standard_answers.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    # 批改结果
    status = Column(String(20), default="pending")  # pending / processing / completed / failed
    total_score = Column(Float)
    max_score = Column(Float, default=10.0)
    step_results = Column(JSON)  # [{"step": 1, "score": 3.0, "max_score": 3.0, "is_correct": true, "comment": "..."}]
    feedback = Column(Text)
    suggestions = Column(JSON)

    processing_time = Column(Float)  # seconds
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

    # 关联
    image = relationship("Image", back_populates="gradings")
    standard_answer = relationship("StandardAnswer", back_populates="gradings")
    user = relationship("User", back_populates="gradings")


# ============== Class Model ==============

class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(String(50), unique=True, index=True, nullable=False)
    class_name = Column(String(100), nullable=False)
    grade = Column(String(50))
    description = Column(Text)
    teacher_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关联
    teacher = relationship("User", back_populates="classes")
    students = relationship("Student", back_populates="class_")
    batch_tasks = relationship("BatchTask", back_populates="class_")


# ============== Student Model ==============

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(50), unique=True, index=True, nullable=False)
    student_name = Column(String(100), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关联
    class_ = relationship("Class", back_populates="students")
    gradings = relationship("Grading", back_populates="student")


# ============== Batch Task Model ==============

class BatchTask(Base):
    __tablename__ = "batch_tasks"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(String(50), unique=True, index=True, nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"))
    standard_answer_id = Column(Integer, ForeignKey("standard_answers.id"))
    total = Column(Integer, default=0)
    pending = Column(Integer, default=0)
    completed = Column(Integer, default=0)
    failed = Column(Integer, default=0)
    status = Column(String(20), default="pending")
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关联
    class_ = relationship("Class", back_populates="batch_tasks")
