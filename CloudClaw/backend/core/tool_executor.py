from typing import Dict, Any
from backend.core.base_tool import BaseTool, RiskLevel
from backend.core.tool_registry import tool_registry
from backend.security.rbac import check_permission
from backend.infrastructure.logger import logger

class ToolExecutor:
    """工具执行器：封装权限校验、风险控制、日志记录，安全调用工具"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id  # 当前调用工具的用户ID，用于权限校验

    async def execute(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        执行指定工具
        :param tool_name: 工具唯一标识
        :param kwargs: 工具入参
        :return: 工具执行结果
        """
        # 1. 获取工具类并实例化
        tool_class = tool_registry.get_tool(tool_name)
        tool: BaseTool = tool_class()
        
        # 2. 权限校验：检查当前用户是否有调用该工具的权限
        for perm in tool.required_permission:
            if not await check_permission(self.user_id, perm):
                raise PermissionError(f"用户 {self.user_id} 无权限调用工具 {tool_name}，缺失权限：{perm}")
        
        # 3. 风险等级提示（高危操作需二次确认，此处简化为日志）
        if tool.risk_level == RiskLevel.HIGH:
            logger.warning(f"⚠️ 高危操作预警：用户 {self.user_id} 调用高危工具 {tool_name} | 参数：{kwargs}")
        
        # 4. 执行工具并记录日志
        logger.info(f"开始执行工具：{tool_name} | 用户：{self.user_id} | 参数：{kwargs}")
        try:
            result = await tool.run(** kwargs)
            logger.info(f"工具执行成功：{tool_name} | 用户：{self.user_id} | 结果：{result}")
            return result
        except Exception as e:
            logger.error(f"工具执行失败：{tool_name} | 用户：{self.user_id} | 错误：{str(e)}")
            raise Exception(f"工具 {tool_name} 执行失败：{str(e)}")