# 高中物理作业智能批改系统

> 软件项目管理课程 · 第 16 题 · 南开大学

基于自然语言理解、计算机视觉和大语言模型的高中物理作业智能批改系统。支持自动识别学生手写/打印物理作业中的文字、公式和示意图，进行推导过程检查和结果验证，并给出评分与详细反馈。

## 系统架构

```
作业图像 → 图像预处理 → 图像分割 → OCR / 公式识别 / 画图分析
                                          ↓
                                    多模态关联
                                          ↓
                                RAG 物理知识库检索
                                          ↓
                                大模型批改 + 智能体
                                          ↓
                                  评分 + 反馈报告
```

## 技术栈

| 模块 | 技术方案 |
|------|----------|
| 图像预处理 | OpenCV |
| 图像分割 | DocLayout-YOLO |
| OCR 文字识别 | PaddleOCR |
| 公式识别 | UniMERNet / Mathpix API |
| 画图分析 | YOLOv8 + 多模态大模型 |
| RAG 知识库 | FAISS + BGE Embedding |
| 大模型批改 | InternLM-Math API |
| 前端界面 | Vue 3 + TypeScript |

## 团队

| 角色 | 姓名 | 职责 |
|------|------|------|
| PM + 技术负责人 | 赵麒杰 | 项目管理、架构设计、前端开发 |
| CV 开发 | 武英文 | 图像预处理、分割、OCR |
| AI 开发 | 李传宇 | 公式识别、画图分析、多模态关联 |
| AI 开发 | 王硕 | RAG 知识库、大模型集成、智能体 |
| 测试/文档 | 代树衡 | 测试、竞品调研、项目文档 |

## 项目文档

- [项目章程](docs/PROJECT-CHARTER.md)
- [产品 Backlog](docs/backlog.md)
- [Sprint 1 计划](docs/Sprint1-计划.md)
- [Sprint 2 计划](docs/Sprint2-计划.md)
- [Sprint 3 计划](docs/Sprint3-计划.md)
- [API 文档](docs/API-文档.md)

## 项目结构

```
physics-homework-grading/
├── backend/                  # FastAPI 后端
│   ├── main.py              # 入口
│   ├── api/                 # API 路由
│   ├── models/              # 数据模型
│   ├── cv/                  # 图像处理模块
│   ├── ai/                  # AI 模块
│   ├── rag/                 # RAG 知识库
│   ├── grader/              # 批改模块
│   └── tests/              # 测试
├── frontend/                 # Vue 3 前端
│   ├── src/
│   │   ├── views/          # 页面组件
│   │   ├── components/     # 通用组件
│   │   ├── stores/        # Pinia 状态
│   │   └── router/        # 路由
│   └── package.json
├── shared/                  # 共享接口定义
├── docs/                    # 项目文档
├── .github/                 # GitHub Actions
└── README.md
```

## 快速开始

### 后端

```bash
cd backend
pip install -r requirements.txt
python main.py
# 访问 http://localhost:8000/docs
```

### 前端

```bash
cd frontend
npm install
npm run dev
# 访问 http://localhost:5173
```

## 里程碑

| 阶段 | 时间 | 目标 |
|------|------|------|
| 项目启动 | 第 1-2 周 | 选题、调研、团队组建 |
| 需求分析 | 第 3-4 周 | 需求细化、用例建模 |
| 系统设计 | 第 5-6 周 | 架构设计、接口定义 |
| Sprint 1 | 第 7-8 周 | 图像预处理 + OCR + 公式识别 |
| Sprint 2 | 第 9-10 周 | RAG + 大模型批改 |
| Sprint 3 | 第 11-12 周 | 画图分析 + 多模态关联 + 智能体 |
| 测试优化 | 第 13 周 | 集成测试、性能优化 |
| 验收交付 | 第 14 周 | 系统演示、项目报告 |

## License

本项目为课程作业，仅供学习交流。
