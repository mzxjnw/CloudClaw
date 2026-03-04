import logging
import os
from logging.handlers import TimedRotatingFileHandler

def setup_logger():
    # 日志保存路径：用户本地数据目录下的 logs 文件夹
    log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/logs"))
    os.makedirs(log_dir, exist_ok=True)
    
    logger = logging.getLogger("cloudclaw")
    logger.setLevel(logging.DEBUG)
    
    # 避免重复添加handler
    if not logger.handlers:
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # 按天切割，保留180天
        file_handler = TimedRotatingFileHandler(
            filename=os.path.join(log_dir, "cloudclaw.log"),
            when="midnight",
            interval=1,
            backupCount=180,
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # 控制台输出
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger

logger = setup_logger()