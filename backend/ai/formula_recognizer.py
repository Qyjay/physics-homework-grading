"""
公式识别引擎模块
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class FormulaRecognitionResult:
    """公式识别结果"""
    region_id: str          # 区域标识
    latex: str              # LaTeX 表达式
    bbox: Tuple[int, int, int, int]  # 边界框 (x1, y1, x2, y2)
    confidence: float       # 置信度


class FormulaRecognizer:
    """Pix2Text 公式识别引擎封装"""

    def __init__(self) -> None:
        self._engine = None

    def _ensure_engine(self) -> None:
        """延迟加载引擎，避免启动时依赖缺失"""
        if self._engine is not None:
            return
        try:
            from pix2text import Pix2Text
        except ImportError as exc:
            raise RuntimeError(
                "pix2text 未安装，请先安装：pip install pix2text"
            ) from exc
        # 初始化公式识别器，只识别公式（不包含文本）
        self._engine = Pix2Text(enable_text=False)

    def _crop_image(self, image_path: str, bbox: Tuple[int, int, int, int]):
        """裁剪图片区域"""
        try:
            import cv2
        except ImportError as exc:
            raise RuntimeError("缺少 opencv-python，无法裁剪区域") from exc

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"无法加载图片: {image_path}")
        x1, y1, x2, y2 = bbox
        roi = img[y1:y2+1, x1:x2+1]
        if roi.size == 0:
            return None
        return roi

    def recognize_from_image(self, image_path: str) -> List[FormulaRecognitionResult]:
        """对整张图片进行公式识别"""
        self._ensure_engine()
        # Pix2Text 的识别结果格式：[ (bbox, latex, confidence), ... ]
        results = self._engine.recognize(image_path)
        return self._parse_raw_results(results)

    def recognize_from_region(
        self, image_path: str, bbox: Tuple[int, int, int, int], region_id: str
    ) -> List[FormulaRecognitionResult]:
        """对指定区域进行公式识别"""
        self._ensure_engine()
        roi = self._crop_image(image_path, bbox)
        if roi is None:
            return []
        # Pix2Text 支持直接传入 numpy 数组
        results = self._engine.recognize(roi)
        parsed = self._parse_raw_results(results)
        # 将局部坐标转换为全局坐标
        x1, y1, _, _ = bbox
        for item in parsed:
            item.region_id = region_id
            rx1, ry1, rx2, ry2 = item.bbox
            item.bbox = (rx1 + x1, ry1 + y1, rx2 + x1, ry2 + y1)
        return parsed

    @staticmethod
    def _parse_raw_results(raw_results) -> List[FormulaRecognitionResult]:
        """解析 Pix2Text 返回的原始数据"""
        results: List[FormulaRecognitionResult] = []
        if not raw_results:
            return results

        for idx, res in enumerate(raw_results, start=1):
            # Pix2Text 返回格式： (bbox, latex, confidence)
            if len(res) < 3:
                continue
            bbox, latex, conf = res
            x1, y1, x2, y2 = map(int, bbox)  # bbox 可能是 [x1,y1,x2,y2]
            results.append(
                FormulaRecognitionResult(
                    region_id=f"formula_{idx:03d}",
                    latex=latex,
                    bbox=(x1, y1, x2, y2),
                    confidence=float(conf),
                )
            )
        return results


# 单例实例
_FORMULA_RECOGNIZER: Optional[FormulaRecognizer] = None


def get_formula_recognizer() -> FormulaRecognizer:
    """获取公式识别器单例"""
    global _FORMULA_RECOGNIZER
    if _FORMULA_RECOGNIZER is None:
        _FORMULA_RECOGNIZER = FormulaRecognizer()
    return _FORMULA_RECOGNIZER


def recognize_formula(
    image_path: str, regions: Optional[List[Dict[str, object]]] = None
) -> List[FormulaRecognitionResult]:
    """
    公式识别快捷函数
    :param image_path: 图片路径
    :param regions: 可选，区域列表，每个区域包含 region_id 和 bbox
    """
    engine = get_formula_recognizer()
    if not regions:
        return engine.recognize_from_image(image_path)

    all_results: List[FormulaRecognitionResult] = []
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


def results_to_dict(results: List[FormulaRecognitionResult]) -> List[Dict[str, object]]:
    """转换为 API 返回格式"""
    payload: List[Dict[str, object]] = []
    for item in results:
        x1, y1, x2, y2 = item.bbox
        payload.append(
            {
                "region_id": item.region_id,
                "latex": item.latex,
                "bbox": {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
                "confidence": round(item.confidence, 4),
            }
        )
    return payload
