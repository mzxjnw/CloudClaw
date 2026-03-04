import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from backend.infrastructure.middleware import request_log_middleware, global_exception_handler
from backend.infrastructure.logger import logger
from backend.storage.database import test_db_connection
from backend.api.im import router as im_router
from backend.api.tool import router as tool_router

# ========== 初始化FastAPI应用 ==========
app = FastAPI(
    title="CloudClaw 本地智能助手",
    description="基于FastAPI的本地智能工具调用助手，支持IM消息接入、工具调用、权限控制",
    version="1.0.0"
)

# ========== 配置跨域（前端调用需要） ==========
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境请指定具体域名，如 ["http://localhost:8080"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== 注册全局中间件 ==========
app.middleware("http")(request_log_middleware)
app.add_exception_handler(Exception, global_exception_handler)

# ========== 注册API路由 ==========
app.include_router(im_router, prefix="/api/im", tags=["IM消息接口"])
app.include_router(tool_router, prefix="/api/tool", tags=["工具调用接口"])

# ========== 健康检查接口 ==========
@app.get("/health", tags=["基础接口"])
async def health_check():
    """服务健康检查"""
    db_ok = test_db_connection()
    status = "healthy" if db_ok else "unhealthy"
    return {
        "status": status,
        "service": "cloudclaw",
        "version": "1.0.0",
        "database": "connected" if db_ok else "disconnected"
    }

# ========== 启动入口 ==========
if __name__ == "__main__":
    logger.info("🚀 启动CloudClaw服务...")
    # 启动FastAPI服务（默认端口8000，可修改）
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # 允许外网访问
        port=8000,
        reload=True,  # 开发模式自动重载
        log_level="info"
    )