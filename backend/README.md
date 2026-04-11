# 后端 (FastAPI)

高中物理作业智能批改系统 - 后端 API 服务

## 技术栈

- **FastAPI** - 高性能 Python Web 框架
- **SQLAlchemy** - ORM
- **PaddleOCR** - 文字识别
- **UniMERNet** - 公式识别
- **FAISS** - 向量数据库
- **InternLM-Math** - 大模型批改

## 项目结构

```
backend/
├── main.py              # FastAPI 入口
├── requirements.txt     # Python 依赖
├── api/                 # API 路由
│   ├── __init__.py     # 路由注册
│   ├── auth.py         # 认证接口
│   ├── images.py       # 图片接口
│   ├── recognition.py  # 识别接口
│   ├── grading.py      # 批改接口
│   ├── answers.py      # 标准答案接口
│   ├── classes.py      # 班级接口
│   ├── batch.py        # 批量处理接口
│   └── history.py      # 历史记录接口
├── models/             # 数据模型
│   ├── __init__.py
│   ├── database.py     # SQLAlchemy 模型
│   └── schemas.py      # Pydantic 模型
├── cv/                  # 计算机视觉模块
│   └── __init__.py
├── ai/                  # AI 模块
│   └── __init__.py
├── rag/                 # RAG 模块
│   └── __init__.py
├── grader/              # 批改模块
│   └── __init__.py
├── tests/               # 测试
│   └── __init__.py
└── uploads/            # 上传文件目录
```

## 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 运行服务

```bash
python main.py
# 或使用 uvicorn
uvicorn main:app --reload
```

### 3. 访问 API 文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 端点

| 模块 | 前缀 | 主要端点 |
|------|------|----------|
| 认证 | /api/v1/auth | POST /register, POST /login, GET /me |
| 图片 | /api/v1/images | POST /upload, POST /{id}/preprocess |
| 识别 | /api/v1/recognition | POST /segment, POST /ocr, POST /formula |
| 批改 | /api/v1/grading | POST /submit, GET /{id}/status, GET /{id}/result |
| 答案 | /api/v1/answers | GET /, POST /, GET /{id}, PUT /{id}, DELETE /{id} |
| 班级 | /api/v1/classes | GET /, POST /, GET /{id}/summary |
| 批量 | /api/v1/batch | POST /, GET /{id}/status |
| 历史 | /api/v1/history | GET /, GET /{id} |

## 测试账号

- 用户名: `zhaoqijie`
- 密码: `password123`

## 开发说明

### 模块开发顺序（参考）

1. **数据库模型** (`models/database.py`) - 定义数据表结构
2. **API 路由** (`api/*.py`) - 定义接口
3. **业务逻辑** (`cv/`, `ai/`, `rag/`, `grader/`) - 实现具体功能

### Mock 模式

在开发阶段，可以使用 Mock 数据进行测试：

```python
# grader/mock_grader.py
def grade_answer(student_answer, standard_answer) -> GradingResult:
    return GradingResult(
        grading_id="mock_001",
        total_score=8.0,
        max_score=10.0,
        ...
    )
```

## License

课程项目 - 仅供学习交流
