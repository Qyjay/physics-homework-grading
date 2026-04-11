"""
认证接口路由
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from jose import JWTError, jwt
import bcrypt
from typing import Optional
import os

# JWT 配置
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24小时

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

router = APIRouter()


# ============== Pydantic Models ==============

# 预先生成的 bcrypt 哈希（用于开发环境测试账号）
# 原始密码: password123
TEST_PASSWORD_HASH = "$2b$12$FSXYtPb07vnYP0DSyjrHieCL57iHdDAp4UZmlb6ZXDKV7NQr2OiUW"

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    role: str = "teacher"


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    user_id: int
    username: str
    email: Optional[str] = None
    role: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class MessageResponse(BaseModel):
    code: int
    message: str
    data: Optional[dict] = None


# ============== 模拟数据存储 ==============

FAKE_USERS_DB = {
    1: {
        "user_id": 1,
        "username": "zhaoqijie",
        "email": "zhaoqijie@nankai.edu.cn",
        "role": "teacher",
        "hashed_password": TEST_PASSWORD_HASH,
        "created_at": "2026-04-11T10:00:00Z"
    }
}


# ============== 辅助函数 ==============

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token 已过期或无效",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    for user in FAKE_USERS_DB.values():
        if user["username"] == username:
            return user
    raise credentials_exception


# ============== API 路由 ==============

@router.post("/register", response_model=MessageResponse)
async def register(user: UserCreate):
    """用户注册"""
    for u in FAKE_USERS_DB.values():
        if u["username"] == user.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )

    new_id = max(FAKE_USERS_DB.keys()) + 1
    new_user = {
        "user_id": new_id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "hashed_password": bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    FAKE_USERS_DB[new_id] = new_user

    return MessageResponse(
        code=200,
        message="注册成功",
        data={
            "user_id": new_id,
            "username": user.username,
            "role": user.role
        }
    )


@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """用户登录"""
    user = None
    for u in FAKE_USERS_DB.values():
        if u["username"] == form_data.username:
            user = u
            break

    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )

    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse(
            user_id=user["user_id"],
            username=user["username"],
            email=user.get("email"),
            role=user["role"]
        )
    )


@router.get("/me", response_model=MessageResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    """获取当前用户信息"""
    return MessageResponse(
        code=200,
        message="success",
        data={
            "user_id": current_user["user_id"],
            "username": current_user["username"],
            "email": current_user.get("email"),
            "role": current_user["role"],
            "created_at": current_user["created_at"]
        }
    )
