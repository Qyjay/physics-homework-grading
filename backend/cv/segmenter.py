"""
图像区域分割模块
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np


def _get_cv2():
    try:
        import cv2
    except Exception as exc:
        raise RuntimeError("缺少 opencv-python/opencv-python-headless 依赖，无法执行分割。") from exc
    return cv2


@dataclass
class Region:
    region_id: str
    type: str
    bbox: Tuple[int, int, int, int]
    confidence: float


def _clamp_bbox(x: int, y: int, w: int, h: int, shape: Tuple[int, int]) -> Tuple[int, int, int, int]:
    height, width = shape
    x1 = max(0, x)
    y1 = max(0, y)
    x2 = min(width - 1, x + w)
    y2 = min(height - 1, y + h)
    return x1, y1, x2, y2


def detect_text_regions(image: np.ndarray) -> List[Region]:
    """连通域分析检测文字区域"""
    cv2 = _get_cv2()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    bw = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 31, 15
    )
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 3))
    merged = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel, iterations=1)

    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(merged, connectivity=8)
    regions: List[Region] = []
    idx = 1
    image_area = image.shape[0] * image.shape[1]
    for i in range(1, num_labels):
        x, y, w, h, area = stats[i]
        if area < 300 or area > image_area * 0.4:
            continue
        ratio = w / max(h, 1)
        if ratio < 1.2:
            continue
        bbox = _clamp_bbox(x, y, w, h, gray.shape)
        confidence = float(min(0.99, 0.6 + area / max(image_area, 1)))
        regions.append(Region(f"reg_t_{idx:03d}", "text", bbox, confidence))
        idx += 1
    return regions


def detect_formula_regions(image: np.ndarray) -> List[Region]:
    """根据高度与像素密度检测公式区域"""
    cv2 = _get_cv2()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    regions: List[Region] = []
    idx = 1
    h_img, w_img = gray.shape
    image_area = h_img * w_img
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h
        if area < 500 or area > image_area * 0.25:
            continue
        roi = bw[y : y + h, x : x + w]
        density = float(np.count_nonzero(roi) / max(area, 1))
        if h < 25 or density < 0.08 or density > 0.65:
            continue
        bbox = _clamp_bbox(x, y, w, h, gray.shape)
        confidence = float(min(0.95, 0.5 + density))
        regions.append(Region(f"reg_f_{idx:03d}", "formula", bbox, confidence))
        idx += 1
    return regions


def detect_diagram_regions(image: np.ndarray) -> List[Region]:
    """根据边缘密度和面积检测图形区域"""
    cv2 = _get_cv2()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 80, 180)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    regions: List[Region] = []
    idx = 1
    h_img, w_img = gray.shape
    image_area = h_img * w_img
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h
        if area < 2000 or area > image_area * 0.8:
            continue
        roi = edges[y : y + h, x : x + w]
        edge_density = float(np.count_nonzero(roi) / max(area, 1))
        if edge_density < 0.03:
            continue
        bbox = _clamp_bbox(x, y, w, h, gray.shape)
        confidence = float(min(0.92, 0.55 + edge_density))
        regions.append(Region(f"reg_d_{idx:03d}", "diagram", bbox, confidence))
        idx += 1
    return regions


def segment_image(image_path: str) -> List[Region]:
    """完整分割流水线"""
    cv2 = _get_cv2()
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"无法加载图片: {image_path}")

    regions = []
    regions.extend(detect_text_regions(image))
    regions.extend(detect_formula_regions(image))
    regions.extend(detect_diagram_regions(image))
    return regions


def regions_to_dict(regions: List[Region]) -> List[Dict[str, object]]:
    """转换为 API 返回格式"""
    payload: List[Dict[str, object]] = []
    for region in regions:
        x1, y1, x2, y2 = region.bbox
        payload.append(
            {
                "region_id": region.region_id,
                "type": region.type,
                "bbox": {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
                "confidence": round(region.confidence, 4),
            }
        )
    return payload
