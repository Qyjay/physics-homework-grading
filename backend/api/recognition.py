"""
识别接口路由
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import os
from api.auth import get_current_user
from ai.formula_recognizer import recognize_formula as ai_recognize_formula
from cv.segmenter import segment_image, regions_to_dict
from cv.ocr_engine import recognize_text as cv_recognize_text, results_to_dict

from ..ai.formula_recognizer import recognize_formula as formula_recognizer, results_to_dict as formula_to_dict

from datetime import datetime
from fastapi import Depends
from ..ai.multimodal_merger import merge_multimodal_results, answer_to_dict
from .models import MergeRequest, Response  # 假设这些模型已定义

router = APIRouter()


def _resolve_image_path(image_id: str) -> str:
    candidates = [
        os.path.join("uploads", f"{image_id}.jpg"),
        os.path.join("uploads", f"{image_id}.jpeg"),
        os.path.join("uploads", f"{image_id}.png"),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    raise HTTPException(status_code=404, detail=f"未找到图片文件: {image_id}")


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
    image_path = _resolve_image_path(request.image_id)
    regions = regions_to_dict(segment_image(image_path))

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
    image_path = _resolve_image_path(request.image_id)
    text_regions = results_to_dict(cv_recognize_text(image_path))

    return Response(
        code=200,
        message="识别完成",
        data={
            "image_id": request.image_id,
            "text_regions": text_regions
        }
    )




@router.post("/formula", response_model=ResponseModel)
async def recognize_formula(
    file: UploadFile = File(...),
    regions: Optional[str] = Form(None)   # 假设 regions 以 JSON 字符串传递
):
    """
    公式识别接口
    """
    # 保存临时文件
    temp_file = await save_upload_file_temporarily(file)
    try:
        # 解析 regions 参数（如果有）
        region_list = None
        if regions:
            region_list = json.loads(regions)

        # 调用真实的公式识别模块
        results = formula_recognizer(temp_file, region_list)

        # 转换为 API 响应格式
        data = formula_to_dict(results)

        return ResponseModel(
            code=0,
            message="success",
            data=data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 清理临时文件
        os.unlink(temp_file)







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
    try:
        # 调用真实的多模态合并逻辑
        student_answer = merge_multimodal_results(
            ocr_results=request.ocr_results,
            formula_results=request.formula_results
        )
        
        # 将 StudentAnswer 转换为原有 API 格式
        text_regions = []
        formula_regions = []
        for elem in student_answer.structured_elements:
            if elem["type"] == "text":
                text_regions.append({
                    "region_id": elem["source_id"],
                    "text": elem["content"],
                    "bbox": elem["bbox"]
                })
            elif elem["type"] == "formula":
                formula_regions.append({
                    "region_id": elem["source_id"],
                    "latex": elem["content"],
                    "bbox": elem["bbox"]
                })
        
        # 构建返回结果（保留 diagram_elements 为空，可由后续扩展）
        result = {
            "image_id": request.image_id,
            "student_answer": {
                "text_regions": text_regions,
                "formula_regions": formula_regions,
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
    except Exception as e:
        # 可根据实际需求返回错误响应
        return Response(
            code=500,
            message=f"整合失败: {str(e)}",
            data=None
        )
