"""
OCR 识别引擎模块
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

def _get_cv2():
    try:
        import cv2
    except Exception as exc:
        raise RuntimeError("缺少 opencv-python/opencv-python-headless 依赖，无法执行区域 OCR。") from exc
    return cv2


@dataclass
class TextRecognitionResult:
    region_id: str
    text: str
    bbox: Tuple[int, int, int, int]
    confidence: float


class OCREngine:
    """PaddleOCR 引擎封装"""

    def __init__(self, use_angle_cls: bool = True, lang: str = "ch") -> None:
        self.use_angle_cls = use_angle_cls
        self.lang = lang
        self._engine = None

    def _ensure_engine(self) -> None:
        if self._engine is not None:
            return
        try:
            from paddleocr import PaddleOCR
        except Exception as exc:
            raise RuntimeError(
                "PaddleOCR 未安装或不可用，请先安装 paddleocr 和 paddlepaddle。"
            ) from exc
        self._engine = PaddleOCR(use_angle_cls=self.use_angle_cls, lang=self.lang)

    def recognize_from_image(self, image_path: str) -> List[TextRecognitionResult]:
        """对整图 OCR"""
        self._ensure_engine()
        raw = self._engine.ocr(image_path, cls=self.use_angle_cls)
        return self._parse_raw_result(raw)

    def recognize_from_region(
        self, image_path: str, bbox: Tuple[int, int, int, int], region_id: str
    ) -> List[TextRecognitionResult]:
        """对指定区域 OCR"""
        self._ensure_engine()
        cv2 = _get_cv2()
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"无法加载图片: {image_path}")
        x1, y1, x2, y2 = bbox
        roi = image[y1 : y2 + 1, x1 : x2 + 1]
        if roi.size == 0:
            return []
        raw = self._engine.ocr(roi, cls=self.use_angle_cls)
        parsed = self._parse_raw_result(raw)
        for item in parsed:
            item.region_id = region_id
            rx1, ry1, rx2, ry2 = item.bbox
            item.bbox = (rx1 + x1, ry1 + y1, rx2 + x1, ry2 + y1)
        return parsed

    @staticmethod
    def _parse_raw_result(raw: List) -> List[TextRecognitionResult]:
        results: List[TextRecognitionResult] = []
        if not raw:
            return results

        lines = raw[0] if isinstance(raw[0], list) else raw
        for idx, line in enumerate(lines, start=1):
            if not line or len(line) < 2:
                continue
            points = line[0]
            text, score = line[1]
            xs = [int(p[0]) for p in points]
            ys = [int(p[1]) for p in points]
            bbox = (min(xs), min(ys), max(xs), max(ys))
            results.append(
                TextRecognitionResult(
                    region_id=f"ocr_{idx:03d}",
                    text=str(text),
                    bbox=bbox,
                    confidence=float(score),
                )
            )
        return results


_OCR_ENGINE: Optional[OCREngine] = None


def get_ocr_engine() -> OCREngine:
    """获取 OCR 引擎单例"""
    global _OCR_ENGINE
    if _OCR_ENGINE is None:
        _OCR_ENGINE = OCREngine()
    return _OCR_ENGINE


def recognize_text(
    image_path: str, regions: Optional[List[Dict[str, object]]] = None
) -> List[TextRecognitionResult]:
    """OCR 快捷函数：支持整图识别或指定区域识别"""
    engine = get_ocr_engine()
    if not regions:
        return engine.recognize_from_image(image_path)

    all_results: List[TextRecognitionResult] = []
    for region in regions:
        region_id = str(region.get("region_id", "region"))
        bbox_data = region.get("bbox", {})
        bbox = (
            int(bbox_data.get("x1", 0)),
            int(bbox_data.get("y1", 0)),
            int(bbox_data.get("x2", 0)),
            int(bbox_data.get("y2", 0)),
        )
        all_results.extend(engine.recognize_from_region(image_path, bbox, region_id))
    return all_results


def results_to_dict(results: List[TextRecognitionResult]) -> List[Dict[str, object]]:
    """转换为 API 返回格式"""
    payload: List[Dict[str, object]] = []
    for item in results:
        x1, y1, x2, y2 = item.bbox
        payload.append(
            {
                "region_id": item.region_id,
                "text": item.text,
                "bbox": {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
                "confidence": round(item.confidence, 4),
            }
        )
    return payload
