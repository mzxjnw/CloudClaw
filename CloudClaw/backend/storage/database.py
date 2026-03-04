import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend.infrastructure.logger import logger

# 数据库文件路径：用户本地数据目录下的 cloudclaw.db
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data"))
os.makedirs(DATA_DIR, exist_ok=True)
DB_FILE = os.path.join(DATA_DIR, "cloudclaw.db")

# SQLite 连接配置（本地文件数据库，无需服务端）
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_FILE}"

# 创建引擎（SQLite 需指定 check_same_thread=False）
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False  # 生产环境关闭 SQL 打印
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 基类：所有 ORM 模型都继承这个
Base = declarative_base()

def get_db():
    """
    数据库会话依赖项：FastAPI 中使用 Depends(get_db) 获取会话
    自动创建表 + 自动关闭会话
    """
    db = SessionLocal()
    try:
        # 确保所有表已创建（首次运行自动建表）
        Base.metadata.create_all(bind=engine)
        yield db
    finally:
        db.close()

# 测试数据库连接
def test_db_connection():
    """测试数据库是否能正常连接，仅用于初始化"""
    try:
        db = next(get_db())
        db.execute("SELECT 1")
        logger.info(f"✅ 数据库连接成功，文件路径：{DB_FILE}")
        return True
    except Exception as e:
        logger.error(f"❌ 数据库连接失败：{str(e)}")
        return False

# 初始化时执行连接测试
test_db_connection()