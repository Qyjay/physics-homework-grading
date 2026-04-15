"""
识别接口路由
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid
from api.auth import get_current_user
from fastapi import APIRouter, Depends
# 导入你创建的公式识别函数
from backend.ai.formula_recognizer import recognize_formula
# 导入你的请求/响应模型（保持你原有定义）
from ... import FormulaRequest, Response, get_current_user

router = APIRouter()


# ============== Pydantic Models ==============

class BoundingBox(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int


class Region(BaseModel):
    region_id: str
    type: str
    bbox: BoundingBox
    confidence: float


class SegmentRequest(BaseModel):
    image_id: str


class OCRRequest(BaseModel):
    image_id: str
    region_ids: Optional[List[str]] = None


class FormulaRequest(BaseModel):
    image_id: str
    region_ids: Optional[List[str]] = None


class DiagramRequest(BaseModel):
    image_id: str
    diagram_type: Optional[str] = "force"


class MergeRequest(BaseModel):
    image_id: str


class Response(BaseModel):
    code: int
    message: str
    data: Optional[dict] = None


# ============== API 路由 ==============

@router.post("/segment", response_model=Response)
async def segment_regions(
    request: SegmentRequest,
    current_user: dict = Depends(get_current_user)
):
    """图像区域分割"""
    # 模拟分割结果
    regions = [
        {
            "region_id": "reg_001",
            "type": "text",
            "bbox": {"x1": 100, "y1": 200, "x2": 500, "y2": 350},
            "confidence": 0.95
        },
        {
            "region_id": "reg_002",
            "type": "formula",
            "bbox": {"x1": 100, "y1": 360, "x2": 500, "y2": 420},
            "confidence": 0.88
        },
        {
            "region_id": "reg_003",
            "type": "diagram",
            "bbox": {"x1": 550, "y1": 200, "x2": 900, "y2": 600},
            "confidence": 0.82
        }
    ]

    return Response(
        code=200,
        message="分割完成",
        data={
            "image_id": request.image_id,
            "regions": regions
        }
    )


@router.post("/ocr", response_model=Response)
async def recognize_text(
    request: OCRRequest,
    current_user: dict = Depends(get_current_user)
):
    """OCR 文字识别"""
    text_regions = [
        {
            "region_id": "reg_001",
            "text": "根据牛顿第二定律，F=ma，可知加速度",
            "bbox": {"x1": 100, "y1": 200, "x2": 500, "y2": 350},
            "confidence": 0.92
        }
    ]

    return Response(
        code=200,
        message="识别完成",
        data={
            "image_id": request.image_id,
            "text_regions": text_regions
        }
    )




@router.post("/formula", response_model=Response)
async def recognize_formula(
    request: FormulaRequest,
    current_user: dict = Depends(get_current_user)
):
    """公式识别"""
    # 调用AI识别模块，替换原有模拟代码
    data = recognize_formula(image_id=request.image_id)

    return Response(
        code=200,
        message="识别完成",
        data=data
    )







@router.post("/diagram", response_model=Response)
async def detect_diagram(
    request: DiagramRequest,
    current_user: dict = Depends(get_current_user)
):
    """图形元素检测"""
    elements = {
        "objects": [
            {"type": "block", "label": "A", "bbox": {"x1": 300, "y1": 400, "x2": 450, "y2": 480}}
        ],
        "forces": [
            {"name": "F", "on": "A", "direction": "right", "magnitude": "10N"},
            {"name": "mg", "on": "A", "direction": "down", "magnitude": "19.6N"},
            {"name": "N", "on": "A", "direction": "up", "magnitude": "19.6N"}
        ],
        "annotations": [
            {"text": "F₁", "position": {"x": 460, "y": 440}},
            {"text": "θ=30°", "position": {"x": 250, "y": 350}}
        ]
    }

    return Response(
        code=200,
        message="检测完成",
        data={
            "image_id": request.image_id,
            "diagram_type": request.diagram_type,
            "elements": elements,
            "confidence": 0.85
        }
    )


@router.post("/merge", response_model=Response)
async def merge_multimodal(
    request: MergeRequest,
    current_user: dict = Depends(get_current_user)
):
    """多模态整合"""
    result = {
        "image_id": request.image_id,
        "student_answer": {
            "text_regions": [
                {"region_id": "reg_001", "text": "根据牛顿第二定律...", "bbox": {}}
            ],
            "formula_regions": [
                {"region_id": "reg_002", "latex": "F = m \\cdot a", "bbox": {}}
            ],
            "diagram_elements": {
                "objects": [],
                "forces": [],
                "annotations": []
            }
        },
        "processed_at": datetime.utcnow().isoformat() + "Z"
    }

    return Response(
        code=200,
        message="整合完成",
        data=result
    )
