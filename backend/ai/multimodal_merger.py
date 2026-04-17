"""
多模态结果整合模块
将 OCR 文本识别结果与公式识别结果按阅读顺序合并为学生答案
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum


class ElementType(str, Enum):
    TEXT = "text"
    FORMULA = "formula"


@dataclass
class StudentAnswer:
    """学生答案结构化数据"""
    raw_text: str                     # 合并后的纯文本（公式为 LaTeX 字符串）
    structured_elements: List[Dict]   # 结构化元素列表，每个元素包含类型、内容、坐标、置信度
    answer_regions: List[Dict]        # 答案所在的区域（可选，按需使用）


@dataclass
class MergedElement:
    """中间合并元素"""
    type: ElementType
    content: str
    bbox: Tuple[int, int, int, int]   # (x1, y1, x2, y2)
    confidence: float
    source_id: str                    # 来源标识（region_id 或其他）


class MultimodalMerger:
    """多模态结果合并器"""

    def __init__(self, reading_order: str = "top-bottom-left-right"):
        """
        :param reading_order: 阅读顺序策略，目前支持 "top-bottom-left-right"
        """
        self.reading_order = reading_order

    def merge(
        self,
        ocr_results: List[Dict],
        formula_results: List[Dict]
    ) -> StudentAnswer:
        """
        整合 OCR 文本和公式识别结果，生成学生答案

        :param ocr_results: OCR 结果列表，每个元素为 dict，至少包含：
                            {"text": str, "bbox": {"x1": int, "y1": int, "x2": int, "y2": int},
                             "confidence": float, "region_id": str}
        :param formula_results: 公式识别结果列表，每个元素为 dict，至少包含：
                                {"latex": str, "bbox": {...}, "confidence": float, "region_id": str}
        :return: StudentAnswer 对象
        """
        # 1. 统一转换为 MergedElement 列表
        elements: List[MergedElement] = []

        for ocr in ocr_results:
            bbox = ocr["bbox"]
            elements.append(
                MergedElement(
                    type=ElementType.TEXT,
                    content=ocr["text"],
                    bbox=(bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"]),
                    confidence=ocr.get("confidence", 1.0),
                    source_id=ocr.get("region_id", "")
                )
            )

        for fm in formula_results:
            bbox = fm["bbox"]
            elements.append(
                MergedElement(
                    type=ElementType.FORMULA,
                    content=fm["latex"],
                    bbox=(bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"]),
                    confidence=fm.get("confidence", 1.0),
                    source_id=fm.get("region_id", "")
                )
            )

        # 2. 按阅读顺序排序
        sorted_elements = self._sort_by_reading_order(elements)

        # 3. 构建原始文本和结构化元素
        raw_text_parts = []
        structured_elements = []

        for elem in sorted_elements:
            # 原始文本构建
            if elem.type == ElementType.TEXT:
                raw_text_parts.append(elem.content)
            else:  # formula
                # 通常公式在上下文中用 $...$ 包裹，或者保留原始 LaTeX
                raw_text_parts.append(f"${elem.content}$")  # 行内公式风格

            # 结构化元素保留详细信息
            structured_elements.append({
                "type": elem.type.value,
                "content": elem.content,
                "bbox": {"x1": elem.bbox[0], "y1": elem.bbox[1],
                         "x2": elem.bbox[2], "y2": elem.bbox[3]},
                "confidence": round(elem.confidence, 4),
                "source_id": elem.source_id
            })

        raw_text = "".join(raw_text_parts)  # 注意：可能需要添加空格或换行，但直接拼接通常足够

        # 可选：简单后处理，避免单词连在一起（如果 OCR 已经包含空格则无需处理）
        # 这里保持简单

        return StudentAnswer(
            raw_text=raw_text,
            structured_elements=structured_elements,
            answer_regions=[]   # 如果需要，可以从输入中提取区域信息
        )

    def _sort_by_reading_order(self, elements: List[MergedElement]) -> List[MergedElement]:
        """
        按照阅读顺序排序：先按 y1 从上到下，y1 相近时按 x1 从左到右。
        使用 y 坐标的“行”分组，容忍一定阈值（例如行高的一半）。
        """
        if not elements:
            return []

        # 复制一份避免修改原列表
        elems = list(elements)

        # 1. 估算平均行高，用于确定哪些元素在同一行
        # 简单方法：计算所有元素高度的中位数
        heights = [bbox[3] - bbox[1] for _, _, _, bbox in [(e.type, e.content, e.confidence, e.bbox) for e in elems]]
        if not heights:
            return elems
        median_height = sorted(heights)[len(heights)//2]
        row_threshold = median_height * 0.6   # 容忍同一行的垂直偏差

        # 2. 按 y1 排序
        elems.sort(key=lambda e: e.bbox[1])

        # 3. 分组为行
        rows = []
        current_row = [elems[0]]
        for e in elems[1:]:
            # 如果当前元素的 y1 与当前行的第一个元素的 y1 差值小于阈值，则视为同一行
            if abs(e.bbox[1] - current_row[0].bbox[1]) <= row_threshold:
                current_row.append(e)
            else:
                # 对当前行按 x1 排序后加入结果
                current_row.sort(key=lambda e2: e2.bbox[0])
                rows.extend(current_row)
                current_row = [e]
        # 处理最后一行
        if current_row:
            current_row.sort(key=lambda e2: e2.bbox[0])
            rows.extend(current_row)

        return rows


# 单例实例
_MERGER: Optional[MultimodalMerger] = None


def get_multimodal_merger() -> MultimodalMerger:
    """获取多模态合并器单例"""
    global _MERGER
    if _MERGER is None:
        _MERGER = MultimodalMerger()
    return _MERGER


def merge_multimodal_results(
    ocr_results: List[Dict],
    formula_results: List[Dict]
) -> StudentAnswer:
    """快捷函数：整合 OCR 和公式识别结果"""
    merger = get_multimodal_merger()
    return merger.merge(ocr_results, formula_results)


def answer_to_dict(answer: StudentAnswer) -> Dict:
    """将 StudentAnswer 转换为 API 响应格式"""
    return {
        "raw_text": answer.raw_text,
        "structured_elements": answer.structured_elements,
        "answer_regions": answer.answer_regions
    }