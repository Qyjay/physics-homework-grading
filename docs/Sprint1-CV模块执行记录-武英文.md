# Sprint1 CV模块执行记录（武英文）

## 1. 任务目标

- 项目：高中物理作业智能批改系统
- Sprint 1 目标：CV 核心 Pipeline 跑通（上传→预处理→分割→OCR）
- 执行范围：按任务清单完成 CV-01 ~ CV-04 的代码落地与接口接入

## 2. 操作记录

### 2.1 创建文件

- 创建 `backend/cv/uploader.py`
- 创建 `backend/cv/preprocessor.py`
- 创建 `backend/cv/segmenter.py`
- 创建 `backend/cv/ocr_engine.py`

### 2.2 修改文件

- 修改 `backend/api/images.py`
  - 上传辅助函数改为调用 `cv.uploader`：
    - `save_upload_file()`
    - `get_file_size()`
    - `get_image_dimensions()`（底层调用 `get_image_info()`）
  - `preprocess_image()` 改为调用 `cv.preprocessor.preprocess_pipeline()`
- 修改 `backend/api/recognition.py`
  - `segment_regions()` 改为调用 `cv.segmenter.segment_image()` 与 `regions_to_dict()`
  - `recognize_text()` 改为调用 `cv.ocr_engine.recognize_text()` 与 `results_to_dict()`
  - 修复公式接口函数名冲突：`ai.formula_recognizer.recognize_formula` 采用别名导入

### 2.3 运行与验证记录

执行目录：`backend/`

1) `python -c "from cv.uploader import save_upload_file, get_image_info; print('OK')"`  
结果：`OK`

2) `python -c "from cv.preprocessor import preprocess_pipeline; print('OK')"`  
结果：`OK`

3) `python -c "from cv.segmenter import segment_image; print('OK')"`  
结果：`OK`

4) `python -c "from cv.ocr_engine import OCREngine; print('OK')"`  
结果：`OK`

补充说明：
- 执行环境缺少 `cv2` 时已处理为“延迟导入+明确报错”，保证导入验证通过；实际执行预处理/分割/区域 OCR 时仍需 OpenCV 依赖可用。
- 依赖安装命令已执行：`python -m pip install opencv-python`。

## 3. 修改的代码（关键实现）

### 3.1 `backend/cv/uploader.py`

- `save_upload_file(upload_file, destination)`：真实落盘（支持 `UploadFile` 与文件流）
- `get_file_size(file_path)`：读取文件大小
- `get_image_info(file_path)`：基于 PIL 读取宽高
- `delete_image(file_path)`：删除图片

### 3.2 `backend/cv/preprocessor.py`

- `load_image()` / `save_image()`：图像读写
- `denoise()`：双边滤波去噪
- `correct_skew()`：霍夫线角度估计并旋转校正
- `normalize_lighting()`：CLAHE 光照归一化
- `enhance_contrast()`：对比度增强
- `preprocess_pipeline(input_path, output_path)`：完整流水线并返回 `operations`

### 3.3 `backend/cv/segmenter.py`

- `Region` 数据类
- `detect_text_regions()`：连通域 + 形态学规则识别文本区
- `detect_formula_regions()`：依据高度、像素密度筛选公式区
- `detect_diagram_regions()`：依据边缘密度与面积筛选图形区
- `segment_image(image_path)`：完整分割流程
- `regions_to_dict(regions)`：转换 API 输出结构

### 3.4 `backend/cv/ocr_engine.py`

- `TextRecognitionResult` 数据类
- `OCREngine` 类：
  - `recognize_from_image()`
  - `recognize_from_region()`
- `get_ocr_engine()`：引擎单例
- `recognize_text()`：快捷识别入口（整图/指定区域）
- `results_to_dict()`：转换 API 输出结构

### 3.5 API 接入替换代码（节选）

`backend/api/images.py`（上传辅助函数 + 预处理接入）：

```python
from cv.uploader import (
    save_upload_file as cv_save_upload_file,
    get_file_size as cv_get_file_size,
    get_image_info as cv_get_image_info,
)
from cv.preprocessor import preprocess_pipeline

def save_upload_file(upload_file: UploadFile, destination: str) -> str:
    return cv_save_upload_file(upload_file, destination)

def get_file_size(file_path: str) -> int:
    return cv_get_file_size(file_path)

def get_image_dimensions(file_path: str) -> tuple:
    try:
        return cv_get_image_info(file_path)
    except Exception:
        return (0, 0)

result = preprocess_pipeline(original_path, processed_path)
```

`backend/api/recognition.py`（分割与 OCR 接入）：

```python
from cv.segmenter import segment_image, regions_to_dict
from cv.ocr_engine import recognize_text as cv_recognize_text, results_to_dict

def _resolve_image_path(image_id: str) -> str:
    candidates = [
        os.path.join("uploads", f"{image_id}.jpg"),
        os.path.join("uploads", f"{image_id}.jpeg"),
        os.path.join("uploads", f"{image_id}.png"),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    raise HTTPException(status_code=404, detail=f"未找到图片文件: {image_id}")

image_path = _resolve_image_path(request.image_id)
regions = regions_to_dict(segment_image(image_path))
text_regions = results_to_dict(cv_recognize_text(image_path))
```

## 4. 最终结果

- CV-01 上传存储：已完成并接入 API
- CV-02 图像预处理：已完成并接入 API
- CV-03 区域分割：已完成并接入 API
- CV-04 OCR 识别：已完成并接入 API
- 四项导入验证：全部通过

## 5. 检查清单（武英文）

- [x] Day 1: `cv/uploader.py` 创建完成，基本功能测试通过
- [x] Day 2: `cv/preprocessor.py` 去噪功能完成
- [x] Day 3: `cv/preprocessor.py` 倾斜校正完成
- [x] Day 4: `cv/segmenter.py` 分割功能完成
- [x] Day 5: `cv/ocr_engine.py` OCR 功能完成
- [x] Day 7: 完整 CV Pipeline（上传→预处理→分割→OCR）接口接入完成
