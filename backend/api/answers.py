"""
标准答案接口路由
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid
from api.auth import get_current_user

router = APIRouter()


# ============== Pydantic Models ==============

class AnswerStep(BaseModel):
    order: int
    description: str
    content: str
    formula: Optional[str] = None
    score: float


class AnswerCreate(BaseModel):
    question_title: str
    subject: str = "physics"
    grade: str = "high_school_1"
    chapter: str
    steps: List[AnswerStep]
    total_score: float
    tags: Optional[List[str]] = None


class AnswerUpdate(BaseModel):
    question_title: Optional[str] = None
    steps: Optional[List[AnswerStep]] = None
    total_score: Optional[float] = None
    tags: Optional[List[str]] = None


class AnswerResponse(BaseModel):
    code: int
    message: str
    data: Optional[dict] = None


# ============== 模拟数据存储 ==============

FAKE_ANSWERS_DB = {
    "ans_001": {
        "answer_id": "ans_001",
        "question_title": "斜面物体受力分析",
        "subject": "physics",
        "grade": "high_school_1",
        "chapter": "Newton's Laws",
        "steps": [
            {"order": 1, "description": "受力分析", "content": "对物体进行受力分析：重力mg、支持力N、摩擦力f", "formula": None, "score": 3.0},
            {"order": 2, "description": "建立方程", "content": "沿斜面方向建立坐标系", "formula": "F - mg·sin(θ) = ma", "score": 4.0},
            {"order": 3, "description": "代入求解", "content": "代入数值求解", "formula": "a = (F - mg·sin(θ))/m", "score": 3.0}
        ],
        "total_score": 10.0,
        "tags": ["力学", "牛顿第二定律", "斜面"],
        "created_by": 1,
        "created_at": "2026-04-11T11:00:00Z"
    }
}


# ============== API 路由 ==============

@router.post("", response_model=AnswerResponse)
async def create_answer(
    answer: AnswerCreate,
    current_user: dict = Depends(get_current_user)
):
    """创建标准答案"""
    answer_id = f"ans_{uuid.uuid4().hex[:12]}"

    new_answer = {
        "answer_id": answer_id,
        "question_title": answer.question_title,
        "subject": answer.subject,
        "grade": answer.grade,
        "chapter": answer.chapter,
        "steps": [s.dict() for s in answer.steps],
        "total_score": answer.total_score,
        "tags": answer.tags or [],
        "created_by": current_user["user_id"],
        "created_at": datetime.utcnow().isoformat() + "Z"
    }

    FAKE_ANSWERS_DB[answer_id] = new_answer

    return AnswerResponse(
        code=200,
        message="创建成功",
        data={
            "answer_id": answer_id,
            "question_title": answer.question_title,
            "created_at": new_answer["created_at"]
        }
    )


@router.get("", response_model=AnswerResponse)
async def list_answers(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    subject: Optional[str] = None,
    grade: Optional[str] = None,
    chapter: Optional[str] = None,
    keyword: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """获取标准答案列表"""
    items = list(FAKE_ANSWERS_DB.values())

    # 过滤
    if subject:
        items = [a for a in items if a["subject"] == subject]
    if grade:
        items = [a for a in items if a["grade"] == grade]
    if chapter:
        items = [a for a in items if a["chapter"] == chapter]

    total = len(items)

    return AnswerResponse(
        code=200,
        message="success",
        data={
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": items[(page-1)*page_size: page*page_size]
        }
    )


@router.get("/{answer_id}", response_model=AnswerResponse)
async def get_answer(
    answer_id: str,
    current_user: dict = Depends(get_current_user)
):
    """获取标准答案详情"""
    if answer_id not in FAKE_ANSWERS_DB:
        raise HTTPException(status_code=404, detail="标准答案不存在")

    return AnswerResponse(
        code=200,
        message="success",
        data=FAKE_ANSWERS_DB[answer_id]
    )


@router.put("/{answer_id}", response_model=AnswerResponse)
async def update_answer(
    answer_id: str,
    answer: AnswerUpdate,
    current_user: dict = Depends(get_current_user)
):
    """更新标准答案"""
    if answer_id not in FAKE_ANSWERS_DB:
        raise HTTPException(status_code=404, detail="标准答案不存在")

    existing = FAKE_ANSWERS_DB[answer_id]

    if answer.question_title is not None:
        existing["question_title"] = answer.question_title
    if answer.steps is not None:
        existing["steps"] = [s.dict() for s in answer.steps]
    if answer.total_score is not None:
        existing["total_score"] = answer.total_score
    if answer.tags is not None:
        existing["tags"] = answer.tags

    return AnswerResponse(
        code=200,
        message="更新成功",
        data=existing
    )


@router.delete("/{answer_id}", response_model=AnswerResponse)
async def delete_answer(
    answer_id: str,
    current_user: dict = Depends(get_current_user)
):
    """删除标准答案"""
    if answer_id not in FAKE_ANSWERS_DB:
        raise HTTPException(status_code=404, detail="标准答案不存在")

    del FAKE_ANSWERS_DB[answer_id]

    return AnswerResponse(
        code=200,
        message="删除成功",
        data=None
    )
