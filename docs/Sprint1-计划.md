# Sprint 0 + Sprint 1 详细计划

> 项目：高中物理作业智能批改系统
> Sprint 0：2026-04-11 ~ 2026-04-17（基础设施搭建）
> Sprint 1：2026-04-18 ~ 2026-05-01（核心Pipeline跑通）
> 团队规模：5 人
> 编制日期：2026-04-11 | 编制人：赵麒杰（PM）

---

## 一、Sprint 0：基础设施搭建（4月11日-4月17日）

**目标**：完成所有并行开发的前置条件

### 1.1 任务分配

| 任务ID | 任务 | 负责人 | 前置依赖 | 产出物 | 截止 |
|--------|------|--------|----------|--------|------|
| T-INF-01 | 前端脚手架搭建 | 赵麒杰 | 无 | Vue3项目结构、package.json | 4月12日 |
| T-INF-02 | 后端脚手架搭建 | 王硕 | 无 | FastAPI项目结构、requirements.txt | 4月12日 |
| T-INF-03 | API接口规范定义 | 王硕 | 无 | OpenAPI/Swagger文档 | 4月13日 |
| T-INF-04 | 数据库模型设计 | 王硕 | API规范 | SQLAlchemy模型代码 | 4月14日 |
| T-INF-05 | CI/CD配置 | 代树衡 | 脚手架 | GitHub Actions配置 | 4月14日 |
| T-INF-06 | 项目文档初始化 | 代树衡 | 无 | docs/目录结构 | 4月12日 |

### 1.2 并行关系

```
赵麒杰 ──→ 前端脚手架 ──→ CI/CD(代树衡)
王硕 ────→ 后端脚手架 ──→ API规范 ──→ 数据库模型
代树衡 ──→ 项目文档初始化（独立）
```

### 1.3 Sprint 0 交付物检查清单

- [ ] `frontend/` Vue3项目可运行 (`npm install && npm run dev`)
- [ ] `backend/` FastAPI项目可运行 (`uvicorn main:app --reload`)
- [ ] API文档可访问 (Swagger UI)
- [ ] GitHub Actions CI配置完成
- [ ] `docs/` 目录结构创建完成

---

## 二、Sprint 1：核心Pipeline跑通（4月18日-5月1日）

**目标**：实现端到端的图像→批改Pipeline

### 2.1 任务分配

#### 武英文（CV模块）— 21 SP

| 任务ID | 任务 | 工作内容 | 产出物 | 截止 |
|--------|------|----------|--------|------|
| T-CV-01 | 图像上传存储 | 支持JPG/PNG上传，存储到本地 | `cv/uploader.py` | 4月20日 |
| T-CV-02 | 图像预处理 | 去噪、倾斜校正、透视变换、光照归一化 | `cv/preprocessor.py` | 4月22日 |
| T-CV-03 | 图像区域分割 | DocLayout-YOLO分割文字/公式/图形区域 | `cv/segmenter.py` | 4月25日 |
| T-CV-04 | OCR文字识别 | PaddleOCR中文手写体识别 | `cv/ocr_engine.py` | 4月27日 |
| T-CV-05 | 单元测试 | CV模块单元测试 | `tests/test_cv.py` | 4月28日 |

#### 李传宇（AI模块-公式）— 13 SP

| 任务ID | 任务 | 工作内容 | 产出物 | 截止 |
|--------|------|----------|--------|------|
| T-AI-01 | 公式识别 | UniMERNet公式→LaTeX | `ai/formula_recognizer.py` | 4月20日 |
| T-AI-02 | 多模态整合 | OCR+公式→结构化JSON | `ai/multimodal_merger.py` | 4月28日 |

#### 王硕（AI模块-批改+后端）— 26 SP

| 任务ID | 任务 | 工作内容 | 产出物 | 截止 |
|--------|------|----------|--------|------|
| T-BE-01 | RAG知识库基础 | FAISS+BGE向量库初始化 | `rag/knowledge_base.py` | 4月22日 |
| T-BE-02 | 大模型接入 | InternLM-Math API集成 | `grader/llm_grader.py` | 4月26日 |
| T-BE-03 | 批改结果生成 | 评分+批注+反馈 | `grader/result_generator.py` | 4月28日 |
| T-BE-04 | API端点 | /upload, /grade, /result | `api/routes.py` | 4月30日 |

#### 赵麒杰（前端）— 16 SP

| 任务ID | 任务 | 工作内容 | 产出物 | 截止 |
|--------|------|----------|--------|------|
| T-FE-01 | 登录注册 | 用户注册/登录页面 | `views/Login.vue` | 4月20日 |
| T-FE-02 | 图片上传 | 拖拽上传+预览 | `views/Upload.vue` | 4月22日 |
| T-FE-03 | 标准答案录入 | 录入表单+评分规则 | `views/AnswerInput.vue` | 4月25日 |
| T-FE-04 | 批改结果展示 | 评分+逐步批注+反馈 | `views/Result.vue` | 4月30日 |
| T-FE-05 | 进度指示 | 处理中/识别中/批改中 | `components/Progress.vue` | 4月24日 |

#### 代树衡（测试/文档）— 8 SP

| 任务ID | 任务 | 工作内容 | 产出物 | 截止 |
|--------|------|----------|--------|------|
| T-TEST-01 | 燃尽图 | Sprint燃尽图更新 | `docs/burndown.md` | 每日 |
| T-TEST-02 | 测试用例 | 测试用例设计 | `tests/test_cases.md` | 4月22日 |
| T-TEST-03 | 集成测试 | 端到端测试 | `tests/integration.py` | 5月1日 |

### 2.2 并行开发关系

```
【武英文 - CV流水线（串行依赖）】
图像上传 → 预处理 → 分割 → OCR
    ↓
公式区域提取 ─────────────────────────────────┐
                                                  ↓
                                             多模态整合 → 大模型批改
                                                  ↓
【李传宇 - 公式识别（独立，可并行）】        结果展示
公式识别 ──────────────────────────────────────┘

【王硕 - RAG+大模型（独立，可并行）】
RAG基础 → 大模型接入 → 批改结果生成
    ↓
API端点

【赵麒杰 - 前端（可先Mock开发）】
登录 → 上传 → 答案录入 → 结果展示
```

### 2.3 关键路径（决定Sprint 1结束时间）

```
CV预处理 → 分割 → OCR ─┬→ 多模态整合 → 大模型批改 → 结果展示（赵麒杰）
     └→ 公式识别 ──────┘
```

**预计Sprint 1结束时间**：5月1日

---

## 三、接口契约（保持不变）

### 3.1 统一项目结构

```
physics-homework-grading/
├── backend/
│   ├── main.py
│   ├── api/routes.py
│   ├── models/schemas.py
│   ├── cv/                    # 武英文
│   │   ├── uploader.py
│   │   ├── preprocessor.py
│   │   ├── segmenter.py
│   │   └── ocr_engine.py
│   ├── ai/                    # 李传宇
│   │   ├── formula_recognizer.py
│   │   └── multimodal_merger.py
│   ├── rag/                   # 王硕
│   │   ├── knowledge_base.py
│   │   └── embeddings.py
│   ├── grader/                # 王硕
│   │   ├── llm_grader.py
│   │   └── result_generator.py
│   └── tests/
├── frontend/                   # 赵麒杰
│   └── src/
│       ├── views/
│       ├── components/
│       ├── stores/
│       ├── api/
│       └── router/
└── shared/
    └── interfaces.py          # 共享接口定义
```

### 3.2 核心接口定义

```python
# shared/interfaces.py
from dataclasses import dataclass
from typing import List
from enum import Enum

class ContentType(Enum):
    TEXT = "text"
    FORMULA = "formula"
    IMAGE = "image"

@dataclass
class BoundingBox:
    x1: int; y1: int; x2: int; y2: int

@dataclass
class TextRegion:
    text: str
    bbox: BoundingBox
    confidence: float

@dataclass
class FormulaRegion:
    latex: str
    bbox: BoundingBox
    confidence: float

@dataclass
class ImageAnalysisResult:
    text_regions: List[TextRegion]
    formula_regions: List[FormulaRegion]
    raw_image_path: str
    processed_at: str

@dataclass
class StandardAnswer:
    steps: List[str]
    total_score: float
    step_scores: List[float]

@dataclass
class GradingResult:
    total_score: float
    max_score: float
    step_results: List[dict]
    feedback: str
```

### 3.3 Mock模式

```python
# grader/mock_grader.py
def grade_answer(student_answer, standard_answer) -> GradingResult:
    return GradingResult(
        total_score=8.0,
        max_score=10.0,
        step_results=[
            {"is_correct": True, "score": 5, "max_score": 5, "comment": "正确"},
            {"is_correct": True, "score": 3, "max_score": 5, "comment": "正确"}
        ],
        feedback="答案基本正确，步骤完整"
    )
```

---

## 四、Git分支策略

```
main
 ├── feature/cv-upload          (武英文)
 ├── feature/cv-preprocess      (武英文)
 ├── feature/cv-segment        (武英文)
 ├── feature/cv-ocr            (武英文)
 ├── feature/ai-formula        (李传宇)
 ├── feature/ai-multimodal     (李传宇)
 ├── feature/rag               (王硕)
 ├── feature/grader            (王硕)
 ├── feature/api               (王硕)
 ├── feature/frontend          (赵麒杰)
 └── feature/test              (代树衡)
```

**规则**：
1. 每天结束前 `git pull main` 同步
2. Feature完成后提PR，PM审查后合并
3. 禁止直接push到main

---

## 五、Sprint会议计划

| 会议 | 时间 | 时长 | 参与者 |
|------|------|------|--------|
| Sprint Planning | 4月11日 | 1小时 | 全体 |
| 每日站会 | 每天 | 15分钟 | 全体 |
| Sprint Review | 5月1日 | 1小时 | 全体 |
| Sprint回顾 | 5月1日 | 30分钟 | 全体 |

---

## 六、交付时间表

| 日期 | 里程碑 | 交付物 |
|------|--------|--------|
| 4月12日 | Sprint 0 脚手架完成 | 前后端项目可运行 |
| 4月14日 | API规范完成 | Swagger文档可用 |
| 4月17日 | Sprint 0 结束 | CI/CD配置完成 |
| 4月22日 | CV预处理+公式识别 | 各自独立可测试 |
| 4月28日 | 多模态整合 | 结构化JSON输出 |
| 5月1日 | Sprint 1 结束 | 端到端Pipeline可运行 |

---

## 七、风险与应对

| 风险 | 概率 | 影响 | 应对 |
|------|------|------|------|
| API调用失败 | 中 | 高 | Mock数据兜底 |
| OCR准确率不足 | 高 | 中 | 大模型校验 |
| 图像质量差 | 中 | 中 | 预处理增强 |
| 沟通不畅 | 低 | 高 | 每日站会 |

---

## 八、成功标准

| 指标 | 目标 | 验证方式 |
|------|------|----------|
| Sprint 0交付 | 前后端可运行 | 运行测试 |
| Pipeline可运行 | 端到端通 | 上传图片测试 |
| OCR准确率 | ≥90% | 抽样验证 |
| 公式识别率 | ≥85% | 抽样验证 |

---

*下次更新：每日站会后*
