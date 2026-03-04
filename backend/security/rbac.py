from typing import Dict, List, Set
from backend.storage.database import get_db
from backend.infrastructure.logger import logger

# 内置默认权限配置（示例，实际从数据库读取）
# 结构：{角色: {权限列表}}
DEFAULT_ROLES = {
    "user": ["file:read", "string:edit", "list:filter", "number:calc"],  # 普通用户：仅读、基础操作
    "admin": ["file:read", "file:write", "string:edit", "list:filter", "number:calc"],  # 管理员：可写
    "super_admin": ["*"]  # 超级管理员：所有权限
}

# 用户-角色映射（示例，实际从数据库读取）
USER_ROLES: Dict[str, str] = {
    "user_001": "user",
    "admin_001": "admin",
    "super_001": "super_admin"
}

def get_user_roles(user_id: str) -> List[str]:
    """
    获取用户所属角色（示例：实际从数据库user_role表读取）
    :param user_id: 用户ID
    :return: 角色列表
    """
    # 模拟数据库查询
    db = next(get_db())
    try:
        # 此处简化为从内置字典读取，实际需查询ORM模型
        role = USER_ROLES.get(user_id, "user")  # 默认普通用户
        logger.info(f"用户 {user_id} 所属角色：{role}")
        return [role]
    finally:
        db.close()

def get_role_permissions(role: str) -> Set[str]:
    """
    获取角色拥有的权限（示例：实际从数据库role_permission表读取）
    :param role: 角色名
    :return: 权限集合
    """
    permissions = DEFAULT_ROLES.get(role, [])
    return set(permissions)

async def check_permission(user_id: str, permission: str) -> bool:
    """
    检查用户是否拥有指定权限
    :param user_id: 用户ID
    :param permission: 权限Key（如 file:write）
    :return: 是否拥有权限
    """
    # 1. 获取用户角色
    roles = get_user_roles(user_id)
    
    # 2. 汇总角色所有权限
    all_permissions = set()
    for role in roles:
        all_permissions.update(get_role_permissions(role))
    
    # 3. 超级管理员拥有所有权限（通配符 *）
    if "*" in all_permissions:
        logger.info(f"用户 {user_id} 是超级管理员，拥有权限 {permission}")
        return True
    
    # 4. 检查指定权限
    has_perm = permission in all_permissions
    if has_perm:
        logger.info(f"用户 {user_id} 拥有权限 {permission}")
    else:
        logger.warning(f"用户 {user_id} 缺失权限 {permission}")
    return has_perm

# 测试权限校验
if __name__ == "__main__":
    import asyncio
    # 测试普通用户调用写文件权限（应返回False）
    result1 = asyncio.run(check_permission("user_001", "file:write"))
    print(f"普通用户file:write权限：{result1}")  # False
    
    # 测试管理员调用写文件权限（应返回True）
    result2 = asyncio.run(check_permission("admin_001", "file:write"))
    print(f"管理员file:write权限：{result2}")  # True
    
    # 测试超级管理员调用任意权限（应返回True）
    result3 = asyncio.run(check_permission("super_001", "any:permission"))
    print(f"超级管理员any:permission权限：{result3}")  # True