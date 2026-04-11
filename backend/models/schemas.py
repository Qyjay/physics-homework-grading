"""
Pydantic 数据模型
用于 API 请求/响应验证
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


# ============== 通用 ==============

class MessageResponse(BaseModel):
    code: int
    message: str
    data: Optional[dict] = None


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


# ============== 用户相关 ==============

class UserRole(str, Enum):
    TEACHER = "teacher"
    STUDENT = "student"


class UserBase(BaseModel):
    username: str = Field(..., min_length=6, max_length=20)
    email: Optional[EmailStr] = None
    role: UserRole = UserRole.TEACHER


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=32)


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    user_id: int
    username: str
    email: Optional[str] = None
    role: str
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


# ============== 图片相关 ==============

class BoundingBox(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int


class ImageUploadResponse(BaseModel):
    image_id: str
    filename: str
    url: str
    size: int
    width: int
    height: int


class PreprocessOperation(BaseModel):
    type: str
    params: dict


class PreprocessResponse(BaseModel):
    image_id: str
    processed_url: str
    operations: List[PreprocessOperation]


# ============== 识别相关 ==============

class ContentType(str, Enum):
    TEXT = "text"
    FORMULA = "formula"
    DIAGRAM = "diagram"


class Region(BaseModel):
    region_id: str
    type: ContentType
    bbox: BoundingBox
    confidence: float


class TextRegion(BaseModel):
    region_id: str
    text: str
    bbox: BoundingBox
    confidence: float


class FormulaRegion(BaseModel):
    region_id: str
    latex: str
    bbox: BoundingBox
    confidence: float


class DiagramElement(BaseModel):
    type: Optional[str] = None
    label: Optional[str] = None
    bbox: Optional[BoundingBox] = None


class ForceInfo(BaseModel):
    name: str
    on: str
    direction: str
    magnitude: Optional[str] = None
    bbox: Optional[BoundingBox] = None


class DiagramAnnotation(BaseModel):
    text: str
    position: dict


class DiagramElements(BaseModel):
    objects: List[DiagramElement]
    forces: List[ForceInfo]
    annotations: List[DiagramAnnotation]


class MergeResult(BaseModel):
    text_regions: List[TextRegion]
    formula_regions: List[FormulaRegion]
    diagram_elements: Optional[DiagramElements] = None


# ============== 批改相关 ==============

class GradingOptions(BaseModel):
    include_diagram: bool = True
    detail_level: str = "detailed"  # simple / detailed


class StepResult(BaseModel):
    step: int
    description: str
    student_answer: str
    is_correct: bool
    score: float
    max_score: float
    comment: Optional[str] = None


class GradingSubmitResponse(BaseModel):
    grading_id: str
    image_id: str
    standard_answer_id: str
    status: str
    total_score: float
    max_score: float
    processing_time: float
    created_at: str


class GradingResultResponse(BaseModel):
    grading_id: str
    total_score: float
    max_score: float
    step_results: List[StepResult]
    feedback: str
    suggestions: Optional[List[str]] = None


# ============== 标准答案相关 ==============

class AnswerStep(BaseModel):
    order: int
    description: str
    content: str
    formula: Optional[str] = None
    score: float


class StandardAnswerCreate(BaseModel):
    question_title: str
    subject: str = "physics"
    grade: str = "high_school_1"
    chapter: str
    steps: List[AnswerStep]
    total_score: float = 10.0
    tags: Optional[List[str]] = None


class StandardAnswerResponse(BaseModel):
    answer_id: str
    question_title: str
    subject: str
    grade: str
    chapter: str
    steps: List[AnswerStep]
    total_score: float
    tags: Optional[List[str]] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class StandardAnswerListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[StandardAnswerResponse]


# ============== 班级相关 ==============

class ClassCreate(BaseModel):
    class_name: str
    grade: str
    description: Optional[str] = None


class ClassResponse(BaseModel):
    class_id: str
    class_name: str
    grade: str
    description: Optional[str] = None
    student_count: int
    teacher: dict
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class StudentSummary(BaseModel):
    student_name: str
    grading_count: int
    average_score: float
    latest_grading_id: Optional[str] = None


class ClassSummaryResponse(BaseModel):
    class_id: str
    class_name: str
    grading_count: int
    average_score: float
    pass_rate: float
    students: List[StudentSummary]


# ============== 批量处理相关 ==============

class BatchCreate(BaseModel):
    class_id: Optional[str] = None
    image_ids: List[str]
    standard_answer_id: str


class BatchItem(BaseModel):
    image_id: str
    grading_id: Optional[str] = None
    status: str


class BatchResponse(BaseModel):
    batch_id: str
    total: int
    pending: int
    completed: int
    failed: int
    status: str
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


# ============== 历史记录相关 ==============

class HistoryItem(BaseModel):
    grading_id: str
    image_id: str
    student_name: Optional[str] = None
    standard_answer_id: str
    question_title: str
    total_score: float
    max_score: float
    created_at: str

    class Config:
        from_attributes = True


class HistoryListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[HistoryItem]
