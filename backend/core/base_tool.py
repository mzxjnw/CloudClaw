from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, Any

class RiskLevel(Enum):
    LOW = 1     # 无风险操作，如文件读取
    MEDIUM = 2  # 中等风险，如文件写入
    HIGH = 3    # 高危操作，如Shell命令、删除文件

class BaseTool:
    # 工具基础信息，子类必须赋值
    name: str = Field(..., description="工具唯一标识，英文小写")
    description: str = Field(..., description="工具功能描述，中文")
    input_schema: BaseModel = Field(..., description="工具入参模型，Pydantic格式")
    output_schema: BaseModel = Field(..., description="工具出参模型，Pydantic格式")
    risk_level: RiskLevel = Field(RiskLevel.LOW, description="工具风险等级")
    required_permission: list[str] = Field(default_factory=list, description="调用所需权限Key列表")

    async def run(self, **kwargs) -> Any:
        """
        工具执行核心逻辑
        :param kwargs: 入参，对应 input_schema 定义的字段
        :return: 执行结果，对应 output_schema 定义的字段
        """
        raise NotImplementedError(f"工具 {self.name} 未实现 run 方法")