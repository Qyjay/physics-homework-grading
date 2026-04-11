"""
批量处理接口路由
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid
from api.auth import get_current_user

router = APIRouter()


# ============== Pydantic Models ==============

class BatchCreate(BaseModel):
    class_id: Optional[str] = None
    image_ids: List[str]
    standard_answer_id: str


class BatchItem(BaseModel):
    image_id: str
    grading_id: Optional[str] = None
    status: str


class Response(BaseModel):
    code: int
    message: str
    data: Optional[dict] = None


# ============== 模拟数据存储 ==============

FAKE_BATCH_DB = {}


# ============== API 路由 ==============

@router.post("", response_model=Response)
async def create_batch(
    batch: BatchCreate,
    current_user: dict = Depends(get_current_user)
):
    """创建批量任务"""
    batch_id = f"batch_{uuid.uuid4().hex[:12]}"

    new_batch = {
        "batch_id": batch_id,
        "class_id": batch.class_id,
        "total": len(batch.image_ids),
        "pending": len(batch.image_ids),
        "completed": 0,
        "failed": 0,
        "status": "pending",
        "created_by": current_user["user_id"],
        "created_at": datetime.utcnow().isoformat() + "Z",
        "items": [
            {"image_id": img_id, "status": "pending"} for img_id in batch.image_ids
        ]
    }

    FAKE_BATCH_DB[batch_id] = new_batch

    return Response(
        code=200,
        message="批量任务已创建",
        data=new_batch
    )


@router.get("/{batch_id}/status", response_model=Response)
async def get_batch_status(
    batch_id: str,
    current_user: dict = Depends(get_current_user)
):
    """查询批量任务状态"""
    if batch_id not in FAKE_BATCH_DB:
        raise HTTPException(status_code=404, detail="批量任务不存在")

    return Response(
        code=200,
        message="success",
        data=FAKE_BATCH_DB[batch_id]
    )
