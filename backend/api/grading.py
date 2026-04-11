"""
批改接口路由
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid
import time
from api.auth import get_current_user

router = APIRouter()


# ============== Pydantic Models ==============

class GradingSubmitRequest(BaseModel):
    image_id: str
    standard_answer_id: str
    options: Optional[dict] = None


class GradingResult(BaseModel):
    grading_id: str
    image_id: str
    standard_answer_id: str
    status: str
    total_score: float
    max_score: float
    processing_time: float
    created_at: str


class StepResult(BaseModel):
    step: int
    description: str
    student_answer: str
    is_correct: bool
    score: float
    max_score: float
    comment: str


class Response(BaseModel):
    code: int
    message: str
    data: Optional[dict] = None


# ============== 模拟数据存储 ==============

FAKE_GRADINGS_DB = {}


# ============== API 路由 ==============

@router.post("/submit", response_model=Response)
async def submit_grading(
    request: GradingSubmitRequest,
    current_user: dict = Depends(get_current_user)
):
    """提交批改"""
    grading_id = f"grd_{uuid.uuid4().hex[:12]}"

    # 模拟批改处理
    start_time = time.time()

    grading_result = {
        "grading_id": grading_id,
        "image_id": request.image_id,
        "standard_answer_id": request.standard_answer_id,
        "status": "completed",
        "total_score": 8.0,
        "max_score": 10.0,
        "processing_time": round(time.time() - start_time + 12.5, 2),
        "created_at": datetime.utcnow().isoformat() + "Z"
    }

    FAKE_GRADINGS_DB[grading_id] = grading_result

    return Response(
        code=200,
        message="批改完成",
        data=grading_result
    )


@router.get("/{grading_id}/status", response_model=Response)
async def get_grading_status(
    grading_id: str,
    current_user: dict = Depends(get_current_user)
):
    """查询批改状态"""
    if grading_id not in FAKE_GRADINGS_DB:
        raise HTTPException(status_code=404, detail="批改记录不存在")

    grading = FAKE_GRADINGS_DB[grading_id]

    steps = [
        {"step": "upload", "status": "completed", "time": 0.3},
        {"step": "preprocess", "status": "completed", "time": 1.2},
        {"step": "segment", "status": "completed", "time": 2.1},
        {"step": "ocr", "status": "completed", "time": 3.5},
        {"step": "formula", "status": "completed", "time": 1.8},
        {"step": "grading", "status": "completed", "time": 3.6}
    ]

    return Response(
        code=200,
        message="success",
        data={
            "grading_id": grading_id,
            "status": grading["status"],
            "progress": 100,
            "steps": steps
        }
    )


@router.get("/{grading_id}/result", response_model=Response)
async def get_grading_result(
    grading_id: str,
    current_user: dict = Depends(get_current_user)
):
    """获取批改结果"""
    if grading_id not in FAKE_GRADINGS_DB:
        raise HTTPException(status_code=404, detail="批改记录不存在")

    grading = FAKE_GRADINGS_DB[grading_id]

    step_results = [
        {
            "step": 1,
            "description": "受力分析",
            "student_answer": "对物体A进行受力分析...",
            "is_correct": True,
            "score": 3.0,
            "max_score": 3.0,
            "comment": "受力分析正确，完整识别了所有外力"
        },
        {
            "step": 2,
            "description": "建立方程",
            "student_answer": "F - mg·sin(θ) = ma",
            "is_correct": True,
            "score": 3.0,
            "max_score": 3.0,
            "comment": "方程建立正确"
        },
        {
            "step": 3,
            "description": "求解计算",
            "student_answer": "a = 2.5 m/s²",
            "is_correct": False,
            "score": 2.0,
            "max_score": 4.0,
            "comment": "计算结果偏小，sin30° 应为 0.5 而非 0.4"
        }
    ]

    return Response(
        code=200,
        message="success",
        data={
            "grading_id": grading_id,
            "total_score": grading["total_score"],
            "max_score": grading["max_score"],
            "step_results": step_results,
            "feedback": "整体解题思路正确，主要错误在第三步的计算。建议复习三角函数基础知识。",
            "suggestions": [
                "重新检查 sinθ 的取值",
                "加强三角函数运算练习"
            ]
        }
    )
