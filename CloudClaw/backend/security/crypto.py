import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from backend.infrastructure.logger import logger

# 加密密钥存储路径（首次运行自动生成）
KEY_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/cloudclaw.key"))
os.makedirs(os.path.dirname(KEY_FILE), exist_ok=True)

def generate_key(password: str = "cloudclaw_default") -> bytes:
    """
    基于密码生成加密密钥（PBKDF2 算法）
    :param password: 基础密码，生产环境建议用户自定义
    :return: 32字节密钥
    """
    salt = b"cloudclaw_salt_2026"  # 固定盐值（生产环境可改为随机）
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))
    return key

def get_fernet() -> Fernet:
    """
    获取加密器实例（首次运行自动生成密钥文件）
    :return: Fernet 加密器
    """
    # 首次运行生成密钥文件
    if not os.path.exists(KEY_FILE):
        key = generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        logger.info(f"✅ 首次运行，已生成加密密钥文件：{KEY_FILE}")
    
    # 读取密钥并创建加密器
    with open(KEY_FILE, "rb") as f:
        key = f.read()
    return Fernet(key)

# 全局加密器实例
fernet = get_fernet()

def encrypt_data(data: str) -> str:
    """
    加密字符串数据
    :param data: 明文
    :return: 加密后的Base64字符串
    """
    try:
        encrypted = fernet.encrypt(data.encode("utf-8"))
        return encrypted.decode("utf-8")
    except Exception as e:
        logger.error(f"数据加密失败：{str(e)}")
        raise Exception(f"加密失败：{str(e)}")

def decrypt_data(encrypted_data: str) -> str:
    """
    解密数据
    :param encrypted_data: 加密后的Base64字符串
    :return: 明文
    """
    try:
        decrypted = fernet.decrypt(encrypted_data.encode("utf-8"))
        return decrypted.decode("utf-8")
    except Exception as e:
        logger.error(f"数据解密失败：{str(e)}")
        raise Exception(f"解密失败：{str(e)}")

# 测试加密解密
if __name__ == "__main__":
    test_data = "测试敏感数据：13812345678"
    encrypted = encrypt_data(test_data)
    decrypted = decrypt_data(encrypted)
    logger.info(f"原文：{test_data}")
    logger.info(f"加密后：{encrypted}")
    logger.info(f"解密后：{decrypted}")
    assert test_data == decrypted, "加密解密不一致！"