"""
图像上传与存储模块
"""

from __future__ import annotations

import os
import shutil
from typing import BinaryIO, Tuple

from fastapi import UploadFile
from PIL import Image


def _ensure_parent_dir(path: str) -> None:
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def save_upload_file(upload_file: UploadFile | BinaryIO, destination: str) -> str:
    """
    保存上传文件到目标路径
    支持 FastAPI UploadFile 或文件流对象
    """
    _ensure_parent_dir(destination)

    if isinstance(upload_file, UploadFile):
        upload_file.file.seek(0)
        with open(destination, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    else:
        upload_file.seek(0)
        with open(destination, "wb") as buffer:
            shutil.copyfileobj(upload_file, buffer)

    return destination


def get_file_size(file_path: str) -> int:
    """获取文件大小（字节）"""
    return os.path.getsize(file_path)


def get_image_info(file_path: str) -> Tuple[int, int]:
    """获取图片宽高信息 (width, height)"""
    with Image.open(file_path) as img:
        return img.size


def delete_image(file_path: str) -> bool:
    """删除图片文件，不存在时返回 False"""
    if not os.path.exists(file_path):
        return False
    os.remove(file_path)
    return True
