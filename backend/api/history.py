"""
历史记录接口路由
"""

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from api.auth import get_current_user

router = APIRouter()


# ============== Pydantic Models ==============

class HistoryItem(BaseModel):
    grading_id: str
    image_id: str
    student_name: Optional[str]
    standard_answer_id: str
    question_title: str
    total_score: float
    max_score: float
    created_at: str


class Response(BaseModel):
    code: int
    message: str
    data: Optional[dict] = None


# ============== 模拟数据存储 ==============

FAKE_HISTORY_DB = {
    "grd_001": {
        "grading_id": "grd_001",
        "image_id": "img_001",
        "student_name": "张三",
        "standard_answer_id": "ans_001",
        "question_title": "斜面物体受力分析",
        "total_score": 8.5,
        "max_score": 10.0,
        "created_at": "2026-04-11T14:30:00Z"
    },
    "grd_002": {
        "grading_id": "grd_002",
        "image_id": "img_002",
        "student_name": "李四",
        "standard_answer_id": "ans_001",
        "question_title": "斜面物体受力分析",
        "total_score": 7.0,
        "max_score": 10.0,
        "created_at": "2026-04-11T14:35:00Z"
    }
}


# ============== API 路由 ==============

@router.get("", response_model=Response)
async def list_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    standard_answer_id: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """获取批改历史"""
    items = list(FAKE_HISTORY_DB.values())

    # 过滤
    if standard_answer_id:
        items = [h for h in items if h["standard_answer_id"] == standard_answer_id]

    total = len(items)

    return Response(
        code=200,
        message="success",
        data={
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": items[(page-1)*page_size: page*page_size]
        }
    )


@router.get("/{grading_id}", response_model=Response)
async def get_history_detail(
    grading_id: str,
    current_user: dict = Depends(get_current_user)
):
    """获取批改历史详情"""
    if grading_id not in FAKE_HISTORY_DB:
        return Response(
            code=404,
            message="历史记录不存在",
            data=None
        )

    return Response(
        code=200,
        message="success",
        data=FAKE_HISTORY_DB[grading_id]
    )
