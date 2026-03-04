import time
from fastapi import Request
from fastapi.responses import JSONResponse
from backend.api.response import ApiResponse
from backend.infrastructure.logger import logger

async def request_log_middleware(request: Request, call_next):
    """全局请求日志中间件"""
    start_time = time.time()
    client_ip = request.client.host if request.client else "unknown"
    
    logger.info(f"收到请求: {request.method} {request.url.path} | IP: {client_ip}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(f"请求完成: {request.method} {request.url.path} | 状态码: {response.status_code} | 耗时: {process_time:.4f}s")
    
    return response

async def global_exception_handler(request: Request, exc: Exception):
    """全局异常捕获中间件：统一返回中文提示，禁止返回堆栈给前端"""
    logger.error(f"系统异常: {request.method} {request.url.path} | 异常信息: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=200,  # 业务状态码在body中体现
        content=ApiResponse(code=500, msg="系统内部错误，请查看日志或稍后重试").model_dump()
    )