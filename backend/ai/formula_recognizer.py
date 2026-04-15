from dataclasses import dataclass
from typing import List, Dict, Optional
from functools import lru_cache

# 定义公式识别结果数据类
@dataclass
class FormulaRecognitionResult:
    region_id: str
    latex: str
    bbox: Dict[str, int]  # {"x1": int, "y1": int, "x2": int, "y2": int}
    confidence: float


# 公式识别器主类
class FormulaRecognizer:
    def __init__(self):
        """初始化公式识别模型（预留模型加载位置）"""
        self.model_loaded = True

    def recognize_from_image(self, image_path: str) -> List[FormulaRecognitionResult]:
        """
        从完整图片中识别所有公式区域
        :param image_path: 图片路径
        :return: 公式识别结果列表
        """
        # 实际项目：此处接入公式识别模型
        # 模拟返回结果
        return [
            FormulaRecognitionResult(
                region_id="reg_002",
                latex="F = m \\cdot a",
                bbox={"x1": 100, "y1": 360, "x2": 500, "y2": 420},
                confidence=0.89
            )
        ]

    def recognize_from_region(self, image_path: str, bbox: Dict[str, int]) -> FormulaRecognitionResult:
        """
        从图片指定区域识别公式
        :param image_path: 图片路径
        :param bbox: 坐标区域 {"x1", "y1", "x2", "y2"}
        :return: 单个公式识别结果
        """
        # 实际项目：裁剪区域后进行公式识别
        return FormulaRecognitionResult(
            region_id="reg_custom",
            latex="F = m \\cdot a",
            bbox=bbox,
            confidence=0.92
        )


# 单例模式：全局唯一的公式识别器
@lru_cache(maxsize=1)
def get_formula_recognizer() -> FormulaRecognizer:
    return FormulaRecognizer()


# 快捷调用函数（API直接使用）
def recognize_formula(image_id: str, image_path: Optional[str] = None) -> Dict:
    """
    快捷识别公式，返回API需要的字典格式
    :param image_id: 图片ID
    :param image_path: 图片路径
    :return: API响应数据字典
    """
    recognizer = get_formula_recognizer()
    results = recognizer.recognize_from_image(image_path or "")
    return results_to_dict(image_id, results)


# 转换为API接口格式
def results_to_dict(image_id: str, results: List[FormulaRecognitionResult]) -> Dict:
    """
    将数据类结果转换为前端需要的字典格式
    :param image_id: 图片ID
    :param results: 识别结果列表
    :return: 标准API数据字典
    """
    return {
        "image_id": image_id,
        "formula_regions": [
            {
                "region_id": res.region_id,
                "latex": res.latex,
                "bbox": res.bbox,
                "confidence": res.confidence
            } for res in results
        ]
    }