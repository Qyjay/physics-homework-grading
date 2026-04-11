"""
高中物理作业智能批改系统 - 后端入口
FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from api import routes
from models.database import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时：创建数据库表
    Base.metadata.create_all(bind=engine)
    # 确保上传目录存在
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("uploads/processed", exist_ok=True)
    yield
    # 关闭时：清理资源（如有需要）


# 创建 FastAPI 应用
app = FastAPI(
    title="高中物理作业智能批改系统",
    description="基于 NLP + CV + LLM 的高中物理作业智能批改 API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(routes, prefix="/api/v1")


@app.get("/")
async def root():
    """根路径健康检查"""
    return {"status": "ok", "service": "physics-homework-grading"}


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
