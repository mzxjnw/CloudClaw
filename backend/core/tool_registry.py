from typing import Dict, Type
from backend.core.base_tool import BaseTool

class ToolRegistry:
    """工具注册中心：管理所有可用工具，支持动态注册和获取"""
    _registry: Dict[str, Type[BaseTool]] = {}

    @classmethod
    def register_tool(cls, tool_class: Type[BaseTool]):
        """
        注册工具类
        :param tool_class: 继承自 BaseTool 的工具类
        """
        if not issubclass(tool_class, BaseTool):
            raise ValueError(f"{tool_class.__name__} 必须继承 BaseTool")
        if tool_class.name in cls._registry:
            raise ValueError(f"工具 {tool_class.name} 已存在，不可重复注册")
        
        cls._registry[tool_class.name] = tool_class
        return tool_class

    @classmethod
    def get_tool(cls, tool_name: str) -> Type[BaseTool]:
        """
        根据工具名获取工具类
        :param tool_name: 工具唯一标识
        :return: 工具类
        """
        tool_class = cls._registry.get(tool_name)
        if not tool_class:
            raise ValueError(f"未找到工具 {tool_name}，请先注册")
        return tool_class

    @classmethod
    def list_tools(cls) -> Dict[str, Type[BaseTool]]:
        """获取所有已注册工具"""
        return cls._registry.copy()

# 全局工具注册器实例
tool_registry = ToolRegistry()