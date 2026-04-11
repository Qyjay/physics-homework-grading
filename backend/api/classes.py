"""
班级管理接口路由
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid
from api.auth import get_current_user

router = APIRouter()


# ============== Pydantic Models ==============

class ClassCreate(BaseModel):
    class_name: str
    grade: str
    description: Optional[str] = None


class StudentInfo(BaseModel):
    student_name: str
    grading_count: int
    average_score: float
    latest_grading_id: Optional[str] = None


class Response(BaseModel):
    code: int
    message: str
    data: Optional[dict] = None


# ============== 模拟数据存储 ==============

FAKE_CLASSES_DB = {
    "cls_001": {
        "class_id": "cls_001",
        "class_name": "高三物理A班",
        "grade": "high_school_3",
        "description": "2026届高三物理A班",
        "student_count": 45,
        "teacher": {"user_id": 1, "username": "zhaoqijie"},
        "created_at": "2026-04-11T08:00:00Z"
    }
}


# ============== API 路由 ==============

@router.post("", response_model=Response)
async def create_class(
    class_data: ClassCreate,
    current_user: dict = Depends(get_current_user)
):
    """创建班级"""
    class_id = f"cls_{uuid.uuid4().hex[:12]}"

    new_class = {
        "class_id": class_id,
        "class_name": class_data.class_name,
        "grade": class_data.grade,
        "description": class_data.description,
        "student_count": 0,
        "teacher": {"user_id": current_user["user_id"], "username": current_user["username"]},
        "created_at": datetime.utcnow().isoformat() + "Z"
    }

    FAKE_CLASSES_DB[class_id] = new_class

    return Response(
        code=200,
        message="创建成功",
        data=new_class
    )


@router.get("", response_model=Response)
async def list_classes(
    current_user: dict = Depends(get_current_user)
):
    """获取班级列表"""
    return Response(
        code=200,
        message="success",
        data={"classes": list(FAKE_CLASSES_DB.values())}
    )


@router.get("/{class_id}", response_model=Response)
async def get_class(
    class_id: str,
    current_user: dict = Depends(get_current_user)
):
    """获取班级详情"""
    if class_id not in FAKE_CLASSES_DB:
        raise HTTPException(status_code=404, detail="班级不存在")

    return Response(
        code=200,
        message="success",
        data=FAKE_CLASSES_DB[class_id]
    )


@router.get("/{class_id}/summary", response_model=Response)
async def get_class_summary(
    class_id: str,
    current_user: dict = Depends(get_current_user)
):
    """获取班级批改汇总"""
    if class_id not in FAKE_CLASSES_DB:
        raise HTTPException(status_code=404, detail="班级不存在")

    cls = FAKE_CLASSES_DB[class_id]

    summary = {
        "class_id": class_id,
        "class_name": cls["class_name"],
        "grading_count": 120,
        "average_score": 7.85,
        "pass_rate": 0.82,
        "students": [
            {"student_name": "张三", "grading_count": 3, "average_score": 8.5, "latest_grading_id": "grd_001"},
            {"student_name": "李四", "grading_count": 3, "average_score": 7.2, "latest_grading_id": "grd_002"},
            {"student_name": "王五", "grading_count": 2, "average_score": 9.0, "latest_grading_id": "grd_003"}
        ]
    }

    return Response(
        code=200,
        message="success",
        data=summary
    )
