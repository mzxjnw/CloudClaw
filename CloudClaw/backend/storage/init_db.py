import os
import shutil
from backend.storage.database import engine, Base, DB_FILE, DATA_DIR
from backend.infrastructure.logger import logger

def init_database(reset: bool = False):
    """
    初始化数据库（首次运行/重置数据库）
    :param reset: 是否重置（删除原有数据库文件）
    """
    # 1. 重置逻辑：删除原有数据库文件
    if reset:
        if os.path.exists(DB_FILE):
            try:
                os.remove(DB_FILE)
                logger.info(f"已删除原有数据库文件：{DB_FILE}")
            except Exception as e:
                logger.error(f"删除数据库文件失败：{str(e)}")
                raise Exception(f"重置数据库失败：{str(e)}")
    
    # 2. 确保数据目录存在
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # 3. 创建所有表（Base.metadata 包含所有 ORM 模型）
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ 数据库表创建成功（首次运行自动创建）")
    except Exception as e:
        logger.error(f"❌ 创建数据库表失败：{str(e)}")
        raise Exception(f"初始化数据库表失败：{str(e)}")

def backup_database(backup_path: str = None):
    """
    备份数据库文件
    :param backup_path: 备份文件路径，默认保存到 data/backup/ 下
    """
    if not os.path.exists(DB_FILE):
        logger.warning("数据库文件不存在，无需备份")
        return
    
    # 默认备份路径
    if not backup_path:
        backup_dir = os.path.join(DATA_DIR, "backup")
        os.makedirs(backup_dir, exist_ok=True)
        backup_filename = f"cloudclaw_backup_{os.path.getmtime(DB_FILE)}.db"
        backup_path = os.path.join(backup_dir, backup_filename)
    
    # 复制数据库文件
    try:
        shutil.copy2(DB_FILE, backup_path)
        logger.info(f"✅ 数据库备份成功，备份文件：{backup_path}")
        return backup_path
    except Exception as e:
        logger.error(f"❌ 数据库备份失败：{str(e)}")
        raise Exception(f"备份数据库失败：{str(e)}")

# 首次运行时自动初始化（非重置）
if __name__ == "__main__":
    init_database(reset=False)