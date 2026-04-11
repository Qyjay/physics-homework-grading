# 高中物理作业智能批改系统 — REST API 文档

> 版本：v1.0.0
> 编制日期：2026-04-11
> 基础路径：`/api/v1`

---

## 一、概述

### 1.1 认证方式

所有接口（除 `/auth/*` 外）均需要携带 JWT Token：

```
Authorization: Bearer <your_jwt_token>
```

### 1.2 请求格式

- Content-Type：`application/json`
- 请求体：JSON 格式

### 1.3 响应格式

```json
{
  "code": 200,
  "message": "success",
  "data": { ... }
}
```

### 1.4 错误码

| code | 说明 |
|------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未认证 / Token 过期 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## 二、认证接口 (Auth)

### 2.1 用户注册

```
POST /api/v1/auth/register
```

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名（6-20字符） |
| password | string | 是 | 密码（8-32字符） |
| email | string | 是 | 邮箱 |
| role | string | 否 | `teacher` / `student`，默认 `teacher` |

**请求示例**

```json
{
  "username": "zhaoqijie",
  "password": "password123",
  "email": "zhaoqijie@nankai.edu.cn",
  "role": "teacher"
}
```

**响应示例**

```json
{
  "code": 200,
  "message": "注册成功",
  "data": {
    "user_id": 1,
    "username": "zhaoqijie",
    "role": "teacher"
  }
}
```

---

### 2.2 用户登录

```
POST /api/v1/auth/login
```

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名 |
| password | string | 是 | 密码 |

**响应示例**

```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 86400,
    "user": {
      "user_id": 1,
      "username": "zhaoqijie",
      "role": "teacher"
    }
  }
}
```

---

### 2.3 获取当前用户信息

```
GET /api/v1/auth/me
```

**响应示例**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "user_id": 1,
    "username": "zhaoqijie",
    "email": "zhaoqijie@nankai.edu.cn",
    "role": "teacher",
    "created_at": "2026-04-11T10:00:00Z"
  }
}
```

---

## 三、图片处理接口 (Image)

### 3.1 上传图片

```
POST /api/v1/images/upload
```

**请求格式**：multipart/form-data

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | file | 是 | 图片文件（JPG/PNG/PDF） |
| student_name | string | 否 | 学生姓名 |

**响应示例**

```json
{
  "code": 200,
  "message": "上传成功",
  "data": {
    "image_id": "img_abc123",
    "filename": "homework_001.jpg",
    "url": "/uploads/img_abc123.jpg",
    "size": 1024000,
    "width": 1920,
    "height": 1080
  }
}
```

---

### 3.2 获取图片

```
GET /api/v1/images/{image_id}
```

**响应**：直接返回图片二进制数据

---

### 3.3 图像预处理

```
POST /api/v1/images/{image_id}/preprocess
```

**响应示例**

```json
{
  "code": 200,
  "message": "预处理完成",
  "data": {
    "image_id": "img_abc123",
    "processed_url": "/uploads/processed/img_abc123.jpg",
    "operations": [
      {"type": "denoise", "params": {"method": "bilateral"}},
      {"type": "deskew", "params": {"angle": -3.5}},
      {"type": "perspective", "params": {}},
      {"type": "normalize", "params": {"method": "CLAHE"}}
    ]
  }
}
```

---

## 四、OCR 与识别接口 (Recognition)

### 4.1 图像区域分割

```
POST /api/v1/recognition/segment
```

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| image_id | string | 是 | 图片ID |

**响应示例**

```json
{
  "code": 200,
  "message": "分割完成",
  "data": {
    "image_id": "img_abc123",
    "regions": [
      {
        "region_id": "reg_001",
        "type": "text",
        "bbox": {"x1": 100, "y1": 200, "x2": 500, "y2": 350},
        "confidence": 0.95
      },
      {
        "region_id": "reg_002",
        "type": "formula",
        "bbox": {"x1": 100, "y1": 360, "x2": 500, "y2": 420},
        "confidence": 0.88
      },
      {
        "region_id": "reg_003",
        "type": "diagram",
        "bbox": {"x1": 550, "y1": 200, "x2": 900, "y2": 600},
        "confidence": 0.82
      }
    ]
  }
}
```

---

### 4.2 OCR 文字识别

```
POST /api/v1/recognition/ocr
```

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| image_id | string | 是 | 图片ID |
| region_ids | string[] | 否 | 指定区域ID，不传则识别全部 |

**响应示例**

```json
{
  "code": 200,
  "message": "识别完成",
  "data": {
    "image_id": "img_abc123",
    "text_regions": [
      {
        "region_id": "reg_001",
        "text": "根据牛顿第二定律，F=ma，可知加速度",
        "bbox": {"x1": 100, "y1": 200, "x2": 500, "y2": 350},
        "confidence": 0.92
      }
    ]
  }
}
```

---

### 4.3 公式识别

```
POST /api/v1/recognition/formula
```

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| image_id | string | 是 | 图片ID |
| region_ids | string[] | 否 | 指定区域ID |

**响应示例**

```json
{
  "code": 200,
  "message": "识别完成",
  "data": {
    "image_id": "img_abc123",
    "formula_regions": [
      {
        "region_id": "reg_002",
        "latex": "F = m \\cdot a",
        "bbox": {"x1": 100, "y1": 360, "x2": 500, "y2": 420},
        "confidence": 0.89
      }
    ]
  }
}
```

---

### 4.4 图形元素检测（受力图）

```
POST /api/v1/recognition/diagram
```

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| image_id | string | 是 | 图片ID |
| diagram_type | string | 否 | `force` / `circuit` / `optical`，默认 `force` |

**响应示例**

```json
{
  "code": 200,
  "message": "检测完成",
  "data": {
    "image_id": "img_abc123",
    "diagram_type": "force",
    "elements": {
      "objects": [
        {"type": "block", "label": "A", "bbox": {"x1": 300, "y1": 400, "x2": 450, "y2": 480}}
      ],
      "forces": [
        {"name": "F", "on": "A", "direction": "right", "magnitude": "10N", "bbox": {}},
        {"name": "mg", "on": "A", "direction": "down", "magnitude": "19.6N", "bbox": {}},
        {"name": "N", "on": "A", "direction": "up", "magnitude": "19.6N", "bbox": {}}
      ],
      "annotations": [
        {"text": "F₁", "position": {"x": 460, "y": 440}},
        {"text": "θ=30°", "position": {"x": 250, "y": 350}}
      ]
    },
    "confidence": 0.85
  }
}
```

---

### 4.5 多模态整合

```
POST /api/v1/recognition/merge
```

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| image_id | string | 是 | 图片ID |

**响应示例**

```json
{
  "code": 200,
  "message": "整合完成",
  "data": {
    "image_id": "img_abc123",
    "student_answer": {
      "text_regions": [
        {"region_id": "reg_001", "text": "根据牛顿第二定律...", "bbox": {}}
      ],
      "formula_regions": [
        {"region_id": "reg_002", "latex": "F = m \\cdot a", "bbox": {}}
      ],
      "diagram_elements": {
        "objects": [],
        "forces": [],
        "annotations": []
      }
    },
    "processed_at": "2026-04-11T10:30:00Z"
  }
}
```

---

## 五、批改接口 (Grading)

### 5.1 提交批改

```
POST /api/v1/grading/submit
```

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| image_id | string | 是 | 图片ID |
| standard_answer_id | string | 是 | 标准答案ID |
| options | object | 否 | 批改选项 |

**options 参数**

| 字段 | 类型 | 说明 |
|------|------|------|
| include_diagram | boolean | 是否分析图形，默认 true |
| detail_level | string | `simple` / `detailed`，默认 `detailed` |

**响应示例**

```json
{
  "code": 200,
  "message": "批改完成",
  "data": {
    "grading_id": "grd_xyz789",
    "image_id": "img_abc123",
    "standard_answer_id": "ans_001",
    "status": "completed",
    "total_score": 8.0,
    "max_score": 10.0,
    "processing_time": 12.5,
    "created_at": "2026-04-11T10:35:00Z"
  }
}
```

---

### 5.2 查询批改状态

```
GET /api/v1/grading/{grading_id}/status
```

**响应示例**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "grading_id": "grd_xyz789",
    "status": "completed",
    "progress": 100,
    "steps": [
      {"step": "upload", "status": "completed", "time": 0.3},
      {"step": "preprocess", "status": "completed", "time": 1.2},
      {"step": "segment", "status": "completed", "time": 2.1},
      {"step": "ocr", "status": "completed", "time": 3.5},
      {"step": "formula", "status": "completed", "time": 1.8},
      {"step": "grading", "status": "completed", "time": 3.6}
    ]
  }
}
```

---

### 5.3 获取批改结果

```
GET /api/v1/grading/{grading_id}/result
```

**响应示例**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "grading_id": "grd_xyz789",
    "total_score": 8.0,
    "max_score": 10.0,
    "step_results": [
      {
        "step": 1,
        "description": "受力分析",
        "student_answer": "对物体A进行受力分析...",
        "is_correct": true,
        "score": 3.0,
        "max_score": 3.0,
        "comment": "受力分析正确，完整识别了所有外力"
      },
      {
        "step": 2,
        "description": "建立方程",
        "student_answer": "F - mg\\sin\\theta = ma",
        "is_correct": true,
        "score": 3.0,
        "max_score": 3.0,
        "comment": "方程建立正确"
      },
      {
        "step": 3,
        "description": "求解计算",
        "student_answer": "a = 2.5 m/s²",
        "is_correct": false,
        "score": 2.0,
        "max_score": 4.0,
        "comment": "计算结果偏小，\\sin30° 应为 0.5 而非 0.4"
      }
    ],
    "feedback": "整体解题思路正确，主要错误在第三步的计算。建议复习三角函数基础知识。",
    "suggestions": [
      "重新检查 \\sin\\theta 的取值",
      "加强三角函数运算练习"
    ]
  }
}
```

---

## 六、标准答案接口 (Answer)

### 6.1 创建标准答案

```
POST /api/v1/answers
```

**请求体**

```json
{
  "question_title": "斜面物体受力分析",
  "subject": "physics",
  "grade": "high_school_1",
  "chapter": "Newton's Laws",
  "steps": [
    {
      "order": 1,
      "description": "受力分析",
      "content": "对物体进行受力分析：重力mg、支持力N、摩擦力f",
      "formula": null,
      "score": 3.0
    },
    {
      "order": 2,
      "description": "建立方程",
      "content": "沿斜面方向建立坐标系",
      "formula": "F - mg\\sin\\theta = ma",
      "score": 4.0
    },
    {
      "order": 3,
      "description": "代入求解",
      "content": "代入数值求解",
      "formula": "a = \\frac{F - mg\\sin\\theta}{m} = 2.5 m/s^2",
      "score": 3.0
    }
  ],
  "total_score": 10.0,
  "tags": ["力学", "牛顿第二定律", "斜面"]
}
```

**响应示例**

```json
{
  "code": 200,
  "message": "创建成功",
  "data": {
    "answer_id": "ans_001",
    "question_title": "斜面物体受力分析",
    "created_at": "2026-04-11T11:00:00Z"
  }
}
```

---

### 6.2 获取标准答案列表

```
GET /api/v1/answers
```

**查询参数**

| 参数 | 类型 | 说明 |
|------|------|------|
| page | int | 页码，默认 1 |
| page_size | int | 每页数量，默认 20 |
| subject | string | 学科筛选 |
| grade | string | 年级筛选 |
| chapter | string | 章节筛选 |
| keyword | string | 关键词搜索 |

**响应示例**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 45,
    "page": 1,
    "page_size": 20,
    "items": [
      {
        "answer_id": "ans_001",
        "question_title": "斜面物体受力分析",
        "subject": "physics",
        "grade": "high_school_1",
        "chapter": "Newton's Laws",
        "total_score": 10.0,
        "step_count": 3,
        "created_at": "2026-04-11T11:00:00Z"
      }
    ]
  }
}
```

---

### 6.3 获取标准答案详情

```
GET /api/v1/answers/{answer_id}
```

---

### 6.4 更新标准答案

```
PUT /api/v1/answers/{answer_id}
```

---

### 6.5 删除标准答案

```
DELETE /api/v1/answers/{answer_id}
```

---

## 七、班级管理接口 (Class)

### 7.1 创建班级

```
POST /api/v1/classes
```

**请求体**

```json
{
  "class_name": "高三物理A班",
  "grade": "high_school_3",
  "description": "2026届高三物理A班"
}
```

---

### 7.2 获取班级列表

```
GET /api/v1/classes
```

---

### 7.3 获取班级详情

```
GET /api/v1/classes/{class_id}
```

**响应示例**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "class_id": "cls_001",
    "class_name": "高三物理A班",
    "grade": "high_school_3",
    "student_count": 45,
    "teacher": {
      "user_id": 1,
      "username": "zhaoqijie"
    },
    "created_at": "2026-04-11T08:00:00Z"
  }
}
```

---

### 7.4 班级批改汇总

```
GET /api/v1/classes/{class_id}/summary
```

**响应示例**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "class_id": "cls_001",
    "class_name": "高三物理A班",
    "grading_count": 120,
    "average_score": 7.85,
    "pass_rate": 0.82,
    "students": [
      {
        "student_name": "张三",
        "grading_count": 3,
        "average_score": 8.5,
        "latest_grading_id": "grd_001"
      }
    ]
  }
}
```

---

## 八、批量处理接口 (Batch)

### 8.1 创建批量任务

```
POST /api/v1/batch
```

**请求体**

```json
{
  "class_id": "cls_001",
  "image_ids": ["img_001", "img_002", "img_003", "img_004", "img_005"],
  "standard_answer_id": "ans_001"
}
```

**响应示例**

```json
{
  "code": 200,
  "message": "批量任务已创建",
  "data": {
    "batch_id": "batch_001",
    "total": 5,
    "pending": 5,
    "completed": 0,
    "failed": 0,
    "status": "pending"
  }
}
```

---

### 8.2 查询批量任务状态

```
GET /api/v1/batch/{batch_id}/status
```

**响应示例**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "batch_id": "batch_001",
    "total": 5,
    "pending": 2,
    "completed": 3,
    "failed": 0,
    "status": "processing",
    "items": [
      {"image_id": "img_001", "grading_id": "grd_001", "status": "completed"},
      {"image_id": "img_002", "grading_id": "grd_002", "status": "completed"},
      {"image_id": "img_003", "grading_id": "grd_003", "status": "completed"},
      {"image_id": "img_004", "status": "pending"},
      {"image_id": "img_005", "status": "pending"}
    ]
  }
}
```

---

## 九、历史记录接口 (History)

### 9.1 获取批改历史

```
GET /api/v1/history
```

**查询参数**

| 参数 | 类型 | 说明 |
|------|------|------|
| page | int | 页码 |
| page_size | int | 每页数量 |
| start_date | string | 开始日期 |
| end_date | string | 结束日期 |
| standard_answer_id | string | 标准答案ID |

---

### 9.2 获取批改历史详情

```
GET /api/v1/history/{grading_id}
```

---

## 十、WebSocket 接口（实时进度）

### 10.1 连接

```
WS /api/v1/ws/grading/{grading_id}
```

**客户端接收消息格式**

```json
{
  "type": "progress",
  "data": {
    "step": "ocr",
    "progress": 60,
    "message": "正在识别文字..."
  }
}
```

**消息类型**

| type | 说明 |
|------|------|
| progress | 进度更新 |
| completed | 批改完成 |
| error | 发生错误 |

---

## 附录：错误码详细说明

| code | 错误信息 | 说明 |
|------|----------|------|
| 40001 | 参数不能为空 | 必填参数缺失 |
| 40002 | 参数格式错误 | 参数类型或格式不对 |
| 40003 | 文件大小超限 | 文件超过 10MB |
| 40004 | 不支持的文件格式 | 仅支持 JPG/PNG/PDF |
| 40101 | Token 已过期 | 请重新登录 |
| 40102 | Token 无效 | Token 格式错误或被篡改 |
| 40301 | 无权限访问 | 非资源所有者 |
| 40401 | 图片不存在 | image_id 不存在 |
| 40402 | 标准答案不存在 | answer_id 不存在 |
| 40403 | 班级不存在 | class_id 不存在 |
| 40404 | 批改记录不存在 | grading_id 不存在 |
| 50001 | 图片处理失败 | 预处理/分割失败 |
| 50002 | OCR 识别失败 | 文字识别失败 |
| 50003 | 公式识别失败 | 公式识别失败 |
| 50004 | 批改服务异常 | 大模型调用失败 |

---

*文档版本：v1.0.0 | 最后更新：2026-04-11*
