import os
from pydantic import BaseModel, Field
from typing import Optional, List
from backend.core.base_tool import BaseTool, RiskLevel
from backend.core.tool_registry import tool_registry
from backend.infrastructure.logger import logger

# ====================== 1. 文件读取工具 ======================
class FileReadInput(BaseModel):
    file_path: str = Field(..., description="文件绝对路径，如 C:/test.txt 或 /home/test.txt")

class FileReadOutput(BaseModel):
    content: str = Field(..., description="文件内容")
    file_size: int = Field(..., description="文件大小（字节）")

@tool_registry.register_tool
class FileReadTool(BaseTool):
    name = "file_read"
    description = "读取本地文本文件内容"
    input_schema = FileReadInput
    output_schema = FileReadOutput
    risk_level = RiskLevel.LOW
    required_permission = ["file:read"]

    async def run(self, file_path: str) -> dict:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            file_size = os.path.getsize(file_path)
            logger.info(f"成功读取文件: {file_path} | 大小: {file_size} 字节")
            return {
                "content": content,
                "file_size": file_size
            }
        except Exception as e:
            logger.error(f"读取文件失败: {file_path} | 错误: {str(e)}")
            raise Exception(f"文件读取失败：{str(e)}")

# ====================== 2. 文件写入工具 ======================
class FileWriteInput(BaseModel):
    file_path: str = Field(..., description="文件绝对路径")
    content: str = Field(..., description="要写入的内容")
    overwrite: bool = Field(False, description="是否覆盖已有文件，默认追加")

class FileWriteOutput(BaseModel):
    success: bool = Field(..., description="是否成功")
    file_path: str = Field(..., description="写入的文件路径")

@tool_registry.register_tool
class FileWriteTool(BaseTool):
    name = "file_write"
    description = "写入内容到本地文本文件（默认追加，可覆盖）"
    input_schema = FileWriteInput
    output_schema = FileWriteOutput
    risk_level = RiskLevel.MEDIUM
    required_permission = ["file:write"]

    async def run(self, file_path: str, content: str, overwrite: bool = False) -> dict:
        try:
            mode = "w" if overwrite else "a"
            with open(file_path, mode, encoding="utf-8") as f:
                f.write(content)
            logger.info(f"成功写入文件: {file_path} | 覆盖模式: {overwrite}")
            return {
                "success": True,
                "file_path": file_path
            }
        except Exception as e:
            logger.error(f"写入文件失败: {file_path} | 错误: {str(e)}")
            raise Exception(f"文件写入失败：{str(e)}")

# ====================== 3. 字符串拼接工具 ======================
class StringConcatInput(BaseModel):
    str1: str = Field(..., description="第一个字符串")
    str2: str = Field(..., description="第二个字符串")
    separator: Optional[str] = Field("", description="拼接分隔符，默认空")

class StringConcatOutput(BaseModel):
    result: str = Field(..., description="拼接后的字符串")

@tool_registry.register_tool
class StringConcatTool(BaseTool):
    name = "string_concat"
    description = "将两个字符串拼接，支持自定义分隔符"
    input_schema = StringConcatInput
    output_schema = StringConcatOutput
    risk_level = RiskLevel.LOW
    required_permission = ["string:edit"]

    async def run(self, str1: str, str2: str, separator: str = "") -> dict:
        result = f"{str1}{separator}{str2}"
        logger.info(f"字符串拼接完成: {str1} + {separator} + {str2} = {result}")
        return {"result": result}

# ====================== 4. 列表筛选工具 ======================
class ListFilterInput(BaseModel):
    items: List[str] = Field(..., description="待筛选的字符串列表")
    keyword: str = Field(..., description="筛选关键词（包含匹配）")

class ListFilterOutput(BaseModel):
    matched_items: List[str] = Field(..., description="匹配的列表项")
    count: int = Field(..., description="匹配数量")

@tool_registry.register_tool
class ListFilterTool(BaseTool):
    name = "list_filter"
    description = "根据关键词筛选字符串列表（包含匹配）"
    input_schema = ListFilterInput
    output_schema = ListFilterOutput
    risk_level = RiskLevel.LOW
    required_permission = ["list:filter"]

    async def run(self, items: List[str], keyword: str) -> dict:
        matched = [item for item in items if keyword in item]
        count = len(matched)
        logger.info(f"列表筛选完成: 关键词 {keyword} | 匹配 {count} 项")
        return {
            "matched_items": matched,
            "count": count
        }

# ====================== 5. 数值计算工具 ======================
class NumberCalcInput(BaseModel):
    num1: float = Field(..., description="第一个数值")
    num2: float = Field(..., description="第二个数值")
    operator: str = Field(..., description="运算符号，支持 + - * /")

class NumberCalcOutput(BaseModel):
    result: float = Field(..., description="计算结果")

@tool_registry.register_tool
class NumberCalcTool(BaseTool):
    name = "number_calc"
    description = "基础数值计算，支持加减乘除"
    input_schema = NumberCalcInput
    output_schema = NumberCalcOutput
    risk_level = RiskLevel.LOW
    required_permission = ["number:calc"]

    async def run(self, num1: float, num2: float, operator: str) -> dict:
        if operator == "+":
            result = num1 + num2
        elif operator == "-":
            result = num1 - num2
        elif operator == "*":
            result = num1 * num2
        elif operator == "/":
            if num2 == 0:
                raise Exception("除数不能为0")
            result = num1 / num2
        else:
            raise Exception(f"不支持的运算符: {operator}，仅支持 + - * /")
        
        logger.info(f"数值计算完成: {num1} {operator} {num2} = {result}")
        return {"result": result}