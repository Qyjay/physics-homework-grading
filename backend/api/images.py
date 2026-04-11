"""
图片接口路由
"""

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import os
import uuid
from api.auth import get_current_user

router = APIRouter()

UPLOAD_DIR = "uploads"
PROCESSED_DIR = "uploads/processed"


# ============== Pydantic Models ==============

class ImageResponse(BaseModel):
    code: int
    message: str
    data: Optional[dict] = None


class BoundingBox(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int


class PreprocessOperation(BaseModel):
    type: str
    params: dict


# ============== 模拟数据存储 ==============

FAKE_IMAGES_DB = {}


# ============== 辅助函数 ==============

def save_upload_file(upload_file: UploadFile, destination: str) -> str:
    """保存上传文件"""
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    with open(destination, "wb") as f:
        content = upload_file.file.read()
        f.write(content)
    return destination


def get_file_size(file_path: str) -> int:
    """获取文件大小"""
    return os.path.getsize(file_path)


def get_image_dimensions(file_path: str) -> tuple:
    """获取图片尺寸"""
    try:
        from PIL import Image
        with Image.open(file_path) as img:
            return img.size  # (width, height)
    except:
        return (0, 0)


# ============== API 路由 ==============

@router.post("/upload", response_model=ImageResponse)
async def upload_image(
    file: UploadFile = File(...),
    student_name: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """上传图片"""
    # 检查文件类型
    allowed_types = ["image/jpeg", "image/png", "application/pdf"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件格式，仅支持: {', '.join(allowed_types)}"
        )

    # 生成唯一 ID
    image_id = f"img_{uuid.uuid4().hex[:12]}"

    # 确定文件扩展名
    ext = "jpg" if file.content_type == "image/jpeg" else "png"
    filename = f"{image_id}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    # 保存文件
    await file.seek(0)
    save_upload_file(file, file_path)

    # 获取文件信息
    size = get_file_size(file_path)
    width, height = get_image_dimensions(file_path)

    # 存储元数据
    FAKE_IMAGES_DB[image_id] = {
        "image_id": image_id,
        "filename": filename,
        "url": f"/uploads/{filename}",
        "size": size,
        "width": width,
        "height": height,
        "student_name": student_name,
        "uploaded_by": current_user["user_id"],
        "uploaded_at": datetime.utcnow().isoformat() + "Z"
    }

    return ImageResponse(
        code=200,
        message="上传成功",
        data=FAKE_IMAGES_DB[image_id]
    )


@router.get("/{image_id}", response_model=ImageResponse)
async def get_image(image_id: str):
    """获取图片信息"""
    if image_id not in FAKE_IMAGES_DB:
        raise HTTPException(status_code=404, detail="图片不存在")

    return ImageResponse(
        code=200,
        message="success",
        data=FAKE_IMAGES_DB[image_id]
    )


@router.post("/{image_id}/preprocess", response_model=ImageResponse)
async def preprocess_image(
    image_id: str,
    current_user: dict = Depends(get_current_user)
):
    """图像预处理"""
    if image_id not in FAKE_IMAGES_DB:
        raise HTTPException(status_code=404, detail="图片不存在")

    image_info = FAKE_IMAGES_DB[image_id]

    # 模拟预处理操作
    operations = [
        {"type": "denoise", "params": {"method": "bilateral"}},
        {"type": "deskew", "params": {"angle": -3.5}},
        {"type": "perspective", "params": {}},
        {"type": "normalize", "params": {"method": "CLAHE"}}
    ]

    # 生成处理后的图片路径
    processed_filename = f"processed_{image_info['filename']}"
    processed_path = os.path.join(PROCESSED_DIR, processed_filename)

    # 复制原图作为处理后的图（实际应该进行真实处理）
    original_path = os.path.join(UPLOAD_DIR, image_info["filename"])
    if os.path.exists(original_path):
        save_upload_file(
            UploadFile(open(original_path, "rb")),
            processed_path
        )

    return ImageResponse(
        code=200,
        message="预处理完成",
        data={
            "image_id": image_id,
            "processed_url": f"/uploads/processed/{processed_filename}",
            "operations": operations
        }
    )
