"""
API 路由模块
统一管理所有 API 路由
"""

from fastapi import APIRouter
from api import auth, images, recognition, grading, answers, classes, batch, history

routes = APIRouter()

# 注册子路由
routes.include_router(auth.router, prefix="/auth", tags=["认证"])
routes.include_router(images.router, prefix="/images", tags=["图片"])
routes.include_router(recognition.router, prefix="/recognition", tags=["识别"])
routes.include_router(grading.router, prefix="/grading", tags=["批改"])
routes.include_router(answers.router, prefix="/answers", tags=["标准答案"])
routes.include_router(classes.router, prefix="/classes", tags=["班级"])
routes.include_router(batch.router, prefix="/batch", tags=["批量处理"])
routes.include_router(history.router, prefix="/history", tags=["历史记录"])
