# Sprint 1 详细任务分解（4月11日-4月17日）

> 项目：高中物理作业智能批改系统
> Sprint 1 目标：CV核心Pipeline跑通（上传→预处理→分割→OCR）
> 编制日期：2026-04-11

---

## 一、任务总览

| 模块 | 用户故事 | 负责人 | 前置依赖 |
|------|---------|--------|----------|
| CV | CV-01 图像上传存储 | 武英文 | Sprint 0 |
| CV | CV-02 图像预处理 | 武英文 | CV-01 |
| CV | CV-03 图像区域分割 | 武英文 | CV-02 |
| CV | CV-04 OCR文字识别 | 武英文 | CV-03 |
| AI | CV-05 公式识别 | 李传宇 | CV-03 |
| AI | AI-01 多模态整合 | 李传宇 | CV-04+CV-05 |
| AI | AI-04 大模型批改接入 | 王硕 | AI-01 |
| AI | AI-05 批改结果生成 | 王硕 | AI-04 |
| FE | FE-01~02 前端界面 | 赵麒杰 | Sprint 0 |

**关键路径**：
```
上传(CV-01) → 预处理(CV-02) → 分割(CV-03) → OCR(CV-04)
                                          ↓
                              公式识别(CV-05) → 多模态整合(AI-01) → 大模型批改(AI-04) → 结果生成(AI-05)
```

---

## 二、武英文 - CV模块

### 任务 1: CV-01 图像上传存储（4月12日）

**目标**：实现真实文件存储

**你的任务**：
1. 创建文件 `backend/cv/uploader.py`
   - 实现 `save_upload_file()` 保存上传文件
   - 实现 `get_file_size()` 获取文件大小
   - 实现 `get_image_info()` 获取图片尺寸
   - 实现 `delete_image()` 删除图片

2. 修改文件 `backend/api/images.py`
   - 第 46-67 行：替换 `save_upload_file`、`get_file_size`、`get_image_dimensions` 函数，调用 `cv.uploader` 模块

3. 验证：
   ```bash
   python -c "from cv.uploader import save_upload_file, get_image_info; print('OK')"
   ```

---

### 任务 2: CV-02 图像预处理（4月13日-14日）

**目标**：实现真实预处理

**你的任务**：
1. 创建文件 `backend/cv/preprocessor.py`
   - 实现 `load_image()` 加载图片
   - 实现 `save_image()` 保存图片
   - 实现 `denoise()` 去噪（双边滤波）
   - 实现 `correct_skew()` 倾斜校正（霍夫变换）
   - 实现 `normalize_lighting()` 光照归一化（CLAHE）
   - 实现 `enhance_contrast()` 对比度增强
   - 实现 `preprocess_pipeline()` 完整流水线

2. 修改文件 `backend/api/images.py`
   - 第 136-175 行 `preprocess_image` 函数：调用 `cv.preprocessor.preprocess_pipeline` 替代模拟代码

3. 验证：
   ```bash
   python -c "from cv.preprocessor import preprocess_pipeline; print('OK')"
   ```

---

### 任务 3: CV-03 图像区域分割（4月15日）

**目标**：实现区域分割

**你的任务**：
1. 创建文件 `backend/cv/segmenter.py`
   - 定义 `Region` 数据类
   - 实现 `detect_text_regions()` 检测文字区域（连通域分析）
   - 实现 `detect_formula_regions()` 检测公式区域（高度和密度）
   - 实现 `detect_diagram_regions()` 检测图形区域（边缘和面积）
   - 实现 `segment_image()` 完整分割流水线
   - 实现 `regions_to_dict()` 转换为API格式

2. 修改文件 `backend/api/recognition.py`
   - 第 62-97 行 `segment_regions` 函数：调用 `cv.segmenter.segment_image` 替代模拟代码

3. 验证：
   ```bash
   python -c "from cv.segmenter import segment_image; print('OK')"
   ```

---

### 任务 4: CV-04 OCR文字识别（4月16日-17日）

**目标**：实现OCR识别

**你的任务**：
1. 创建文件 `backend/cv/ocr_engine.py`
   - 定义 `TextRecognitionResult` 数据类
   - 实现 `OCREngine` 类
   - 实现 `recognize_from_image()` 从图片识别文字
   - 实现 `recognize_from_region()` 从指定区域识别
   - 实现 `get_ocr_engine()` 引擎单例
   - 实现 `recognize_text()` 快捷函数
   - 实现 `results_to_dict()` 转换为API格式

2. 修改文件 `backend/api/recognition.py`
   - 第 100-122 行 `recognize_text` 函数：调用 `cv.ocr_engine.recognize_text` 替代模拟代码

3. 安装依赖（如未安装）：
   ```bash
   pip install paddleocr paddlepaddle
   ```

4. 验证：
   ```bash
   python -c "from cv.ocr_engine import OCREngine; print('OK')"
   ```

---

## 三、李传宇 - AI模块

### 任务 1: CV-05 公式识别（4月15日-16日）

**目标**：实现公式识别

**你的任务**：
1. 创建文件 `backend/ai/formula_recognizer.py`
   - 定义 `FormulaRecognitionResult` 数据类
   - 实现 `FormulaRecognizer` 类
   - 实现 `recognize_from_image()` 从图片识别公式
   - 实现 `recognize_from_region()` 从指定区域识别
   - 实现 `get_formula_recognizer()` 识别器单例
   - 实现 `recognize_formula()` 快捷函数
   - 实现 `results_to_dict()` 转换为API格式

2. 修改文件 `backend/api/recognition.py`
   - 第 125-147 行 `recognize_formula` 函数：调用 `ai.formula_recognizer.recognize_formula` 替代模拟代码

3. 验证：
   ```bash
   python -c "from ai.formula_recognizer import FormulaRecognizer; print('OK')"
   ```

---

### 任务 2: AI-01 多模态整合（4月17日）

**目标**：整合多模态识别结果

**你的任务**：
1. 创建文件 `backend/ai/multimodal_merger.py`
   - 定义 `StudentAnswer` 数据类
   - 实现 `MultimodalMerger` 类
   - 实现 `merge()` 整合多模态结果
   - 实现 `_build_raw_text()` 按阅读顺序构建文本
   - 实现 `merge_multimodal_results()` 快捷函数

2. 修改文件 `backend/api/recognition.py`
   - 第 183-211 行 `merge_multimodal` 函数：调用 `ai.multimodal_merger.merge_multimodal_results` 替代模拟代码

3. 验证：
   ```bash
   python -c "from ai.multimodal_merger import MultimodalMerger; print('OK')"
   ```

---

## 四、王硕 - 批改模块

### 任务 1: AI-04 大模型批改接入（4月16日-17日）

**目标**：接入大模型进行批改

**你的任务**：
1. 创建文件 `backend/grader/llm_grader.py`
   - 定义 `GradingPrompt` 提示词类
   - 实现 `LLMGrader` 类
   - 实现 `_build_prompt()` 构建批改提示词
   - 实现 `_call_api()` 调用InternLM API
   - 实现 `_parse_json_response()` 解析API响应
   - 实现 `grade()` 执行批改
   - 实现 `grade_answer()` 快捷函数
   - **注意**：无API Key时使用 `_mock_grade()` 返回模拟结果

2. 修改文件 `backend/api/grading.py`
   - 添加导入 `from grader.llm_grader import grade_answer`
   - 第 58-86 行 `submit_grading` 函数：调用 `grade_answer` 替代模拟数据

3. 验证：
   ```bash
   python -c "from grader.llm_grader import LLMGrader; print('OK')"
   ```

---

### 任务 2: AI-05 批改结果生成（4月17日）

**目标**：生成格式化批改报告

**你的任务**：
1. 创建文件 `backend/grader/result_generator.py`
   - 定义 `StepGradeResult` 数据类
   - 定义 `GradingReport` 数据类
   - 实现 `ResultGenerator` 类
   - 实现 `generate()` 生成批改报告
   - 实现 `_generate_feedback()` 生成反馈文本
   - 实现 `to_dict()` 转换为API格式
   - 实现 `generate_grading_report()` 快捷函数

2. 修改文件 `backend/api/grading.py`
   - 添加导入 `from grader.result_generator import generate_grading_report`
   - 第 121-176 行 `get_grading_result` 函数：使用 `generate_grading_report` 生成报告

3. 验证：
   ```bash
   python -c "from grader.result_generator import ResultGenerator; print('OK')"
   ```

---

## 五、代树衡 - 测试工作

### 任务 1: 单元测试设计（4月12日-14日）

**目标**：为CV模块编写单元测试

**你的任务**：
1. 创建文件 `backend/tests/test_cv.py`
   - 实现 `TestPreprocessor` 测试类
     - `test_load_image()` 测试图片加载
     - `test_denoise()` 测试去噪
     - `test_normalize_lighting()` 测试光照归一化
   - 实现 `TestSegmenter` 测试类
     - `test_segment_image()` 测试图像分割
   - 实现 `TestOCREngine` 测试类
     - `test_ocr_engine_init()` 测试OCR引擎初始化

2. 创建测试图片目录：
   ```bash
   mkdir -p backend/tests/test_images
   ```

3. 运行测试：
   ```bash
   cd backend
   python -m pytest tests/test_cv.py -v
   ```

---

### 任务 2: 集成测试设计（4月15日-17日）

**目标**：为完整Pipeline编写集成测试

**你的任务**：
1. 创建文件 `backend/tests/test_integration.py`
   - 实现 `TestPipeline` 测试类
     - `test_cv_pipeline()` 测试CV处理流水线（预处理→分割→OCR）
     - `test_ai_pipeline()` 测试AI处理流水线（公式识别→多模态整合）
     - `test_grader_pipeline()` 测试批改流水线

2. 运行集成测试：
   ```bash
   cd backend
   python -m pytest tests/test_integration.py -v
   ```

---

## 六、每日站会检查清单

### 武英文
- [ ] Day 1: `cv/uploader.py` 创建完成，基本功能测试通过
- [ ] Day 2: `cv/preprocessor.py` 去噪功能完成
- [ ] Day 3: `cv/preprocessor.py` 倾斜校正完成
- [ ] Day 4: `cv/segmenter.py` 分割功能完成
- [ ] Day 5: `cv/ocr_engine.py` OCR功能完成
- [ ] Day 7: 完整CV Pipeline联调通过

### 李传宇
- [ ] Day 4: `ai/formula_recognizer.py` 创建完成
- [ ] Day 5: `ai/formula_recognizer.py` 测试通过
- [ ] Day 7: `ai/multimodal_merger.py` 多模态整合完成

### 王硕
- [ ] Day 4: `grader/llm_grader.py` 创建完成
- [ ] Day 5: `grader/llm_grader.py` API调用测试
- [ ] Day 7: `grader/result_generator.py` 结果生成完成

### 代树衡
- [ ] Day 1: `tests/test_cv.py` 框架搭建
- [ ] Day 3: CV模块单元测试覆盖 >80%
- [ ] Day 5: `tests/test_integration.py` 框架搭建
- [ ] Day 7: 集成测试覆盖 >60%

---

## 七、文件路径速查表

| 模块 | 文件路径 | 负责人 |
|------|----------|--------|
| CV上传 | `backend/cv/uploader.py` | 武英文 |
| CV预处理 | `backend/cv/preprocessor.py` | 武英文 |
| CV分割 | `backend/cv/segmenter.py` | 武英文 |
| CV-OCR | `backend/cv/ocr_engine.py` | 武英文 |
| AI公式 | `backend/ai/formula_recognizer.py` | 李传宇 |
| AI整合 | `backend/ai/multimodal_merger.py` | 李传宇 |
| LLM批改 | `backend/grader/llm_grader.py` | 王硕 |
| 结果生成 | `backend/grader/result_generator.py` | 王硕 |
| CV测试 | `backend/tests/test_cv.py` | 代树衡 |
| 集成测试 | `backend/tests/test_integration.py` | 代树衡 |
| API路由 | `backend/api/recognition.py` | （按需修改调用CV/AI模块）|

---

*编制人：赵麒杰*
*日期：2026-04-11*
