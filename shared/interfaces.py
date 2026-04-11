"""
共享接口定义
所有模块必须遵循此接口契约

用于：
- 后端 FastAPI 模型定义
- 前端 TypeScript 类型定义
- 模块间数据交换格式
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class ContentType(str, Enum):
    """内容区域类型"""
    TEXT = "text"
    FORMULA = "formula"
    DIAGRAM = "diagram"


@dataclass
class BoundingBox:
    """检测区域坐标"""
    x1: int
    y1: int
    x2: int
    y2: int


@dataclass
class TextRegion:
    """文字识别结果"""
    region_id: str
    text: str
    bbox: BoundingBox
    confidence: float


@dataclass
class FormulaRegion:
    """公式识别结果"""
    region_id: str
    latex: str
    bbox: BoundingBox
    confidence: float


@dataclass
class DiagramObject:
    """图形中的物体"""
    type: str
    label: Optional[str] = None
    bbox: Optional[BoundingBox] = None


@dataclass
class ForceInfo:
    """力的信息"""
    name: str
    on: str  # 作用于哪个物体
    direction: str  # 方向
    magnitude: Optional[str] = None
    bbox: Optional[BoundingBox] = None


@dataclass
class DiagramAnnotation:
    """图形标注"""
    text: str
    position: dict  # {"x": int, "y": int}


@dataclass
class DiagramElements:
    """图形元素集合"""
    objects: List[DiagramObject]
    forces: List[ForceInfo]
    annotations: List[DiagramAnnotation]


@dataclass
class ImageAnalysisResult:
    """图像分析最终结果（CV/AI 模块必须输出此格式）"""
    image_id: str
    text_regions: List[TextRegion]
    formula_regions: List[FormulaRegion]
    diagram_elements: Optional[DiagramElements] = None
    raw_image_path: str
    processed_at: str  # ISO 时间戳


@dataclass
class AnswerStep:
    """标准答案步骤"""
    order: int
    description: str
    content: str
    formula: Optional[str] = None
    score: float


@dataclass
class StandardAnswer:
    """标准答案结构"""
    answer_id: str
    question_title: str
    subject: str = "physics"
    grade: str = "high_school_1"
    chapter: str = ""
    steps: List[AnswerStep] = None
    total_score: float = 10.0
    tags: Optional[List[str]] = None

    def __post_init__(self):
        if self.steps is None:
            self.steps = []


@dataclass
class StepGradingResult:
    """步骤批改结果"""
    step: int
    description: str
    student_answer: str
    is_correct: bool
    score: float
    max_score: float
    comment: Optional[str] = None


@dataclass
class GradingResult:
    """批改结果（grader 模块必须输出此格式）"""
    grading_id: str
    image_id: str
    standard_answer_id: str
    total_score: float
    max_score: float
    step_results: List[StepGradingResult]
    feedback: str
    suggestions: Optional[List[str]] = None
    processing_time: Optional[float] = None
    status: str = "completed"


@dataclass
class APIResponse:
    """统一 API 响应格式"""
    code: int
    message: str
    data: Optional[dict] = None


# ==================== API 接口契约 ====================

# 预处理接口 (cv/preprocessor.py)
def preprocess_image(image_path: str) -> str:
    """
    输入：原始图片路径
    输出：预处理后的图片路径
    """
    ...


# 分割接口 (cv/segmenter.py)
def segment_regions(image_path: str) -> List[BoundingBox]:
    """
    输入：预处理后的图片路径
    输出：文字/公式/图形区域坐标列表
    """
    ...


# OCR 接口 (cv/ocr_engine.py)
def recognize_text(image_path: str, regions: List[BoundingBox]) -> List[TextRegion]:
    """
    输入：图片路径 + 区域坐标
    输出：文字识别结果列表
    """
    ...


# 公式识别接口 (ai/formula_recognizer.py)
def recognize_formula(image_path: str, regions: List[BoundingBox]) -> List[FormulaRegion]:
    """
    输入：图片路径 + 区域坐标
    输出：公式识别结果列表（LaTeX 格式）
    """
    ...


# 多模态关联接口 (ai/multimodal_merger.py)
def merge_multimodal(
    image_id: str,
    text_regions: List[TextRegion],
    formula_regions: List[FormulaRegion],
    diagram_elements: Optional[DiagramElements] = None
) -> ImageAnalysisResult:
    """
    输入：文字区域 + 公式区域 + 图形区域
    输出：结构化的图像分析结果
    """
    ...


# 大模型批改接口 (grader/llm_grader.py)
def grade_answer(
    image_analysis: ImageAnalysisResult,
    standard_answer: StandardAnswer
) -> GradingResult:
    """
    输入：学生答案（结构化）+ 标准答案
    输出：批改结果
    """
    ...
