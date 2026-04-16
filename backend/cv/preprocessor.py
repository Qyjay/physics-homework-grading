"""
图像预处理模块
"""

from __future__ import annotations

import os
from typing import Dict, List, Tuple

import numpy as np


def _get_cv2():
    try:
        import cv2
    except Exception as exc:
        raise RuntimeError("缺少 opencv-python/opencv-python-headless 依赖，无法执行预处理。") from exc
    return cv2


def load_image(image_path: str) -> np.ndarray:
    """加载图片（BGR）"""
    cv2 = _get_cv2()
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"无法加载图片: {image_path}")
    return image


def save_image(image: np.ndarray, output_path: str) -> str:
    """保存图片"""
    cv2 = _get_cv2()
    parent = os.path.dirname(output_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    ok = cv2.imwrite(output_path, image)
    if not ok:
        raise ValueError(f"保存图片失败: {output_path}")
    return output_path


def denoise(image: np.ndarray) -> np.ndarray:
    """双边滤波去噪"""
    cv2 = _get_cv2()
    return cv2.bilateralFilter(image, d=9, sigmaColor=75, sigmaSpace=75)


def _compute_skew_angle(gray: np.ndarray) -> float:
    cv2 = _get_cv2()
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi / 180,
        threshold=100,
        minLineLength=max(50, gray.shape[1] // 10),
        maxLineGap=20,
    )
    if lines is None:
        return 0.0

    angles: List[float] = []
    for line in lines[:, 0]:
        x1, y1, x2, y2 = line
        angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
        if -45 <= angle <= 45:
            angles.append(float(angle))
    if not angles:
        return 0.0
    return float(np.median(angles))


def correct_skew(image: np.ndarray) -> Tuple[np.ndarray, float]:
    """霍夫线变换估计倾斜角并旋转校正"""
    cv2 = _get_cv2()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    angle = _compute_skew_angle(gray)

    if abs(angle) < 0.5:
        return image, 0.0

    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        image,
        matrix,
        (w, h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE,
    )
    return rotated, angle


def normalize_lighting(image: np.ndarray) -> np.ndarray:
    """CLAHE 光照归一化"""
    cv2 = _get_cv2()
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l2 = clahe.apply(l)
    merged = cv2.merge((l2, a, b))
    return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)


def enhance_contrast(image: np.ndarray) -> np.ndarray:
    """对比度增强"""
    cv2 = _get_cv2()
    return cv2.convertScaleAbs(image, alpha=1.2, beta=8)


def preprocess_pipeline(input_path: str, output_path: str) -> Dict[str, object]:
    """完整预处理流水线"""
    image = load_image(input_path)
    operations: List[Dict[str, object]] = []

    image = denoise(image)
    operations.append({"type": "denoise", "params": {"method": "bilateral"}})

    image, angle = correct_skew(image)
    operations.append({"type": "deskew", "params": {"angle": round(angle, 2)}})

    image = normalize_lighting(image)
    operations.append({"type": "normalize", "params": {"method": "CLAHE"}})

    image = enhance_contrast(image)
    operations.append({"type": "enhance_contrast", "params": {"alpha": 1.2, "beta": 8}})

    save_image(image, output_path)

    return {
        "processed_path": output_path,
        "operations": operations,
    }
