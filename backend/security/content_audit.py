import re
from typing import List, Tuple
from backend.infrastructure.logger import logger

# 内置敏感词库（示例，生产环境可扩展）
SENSITIVE_WORDS = [
    # 涉政敏感词（示例）
    "敏感政治词汇1", "敏感政治词汇2",
    # 违规内容词
    "违规内容1", "违规内容2",
    # 恶意指令词
    "rm -rf", "格式化磁盘", "删除系统文件"
]

# 敏感信息正则（手机号、身份证、银行卡）
PHONE_PATTERN = re.compile(r'1[3-9]\d{9}')  # 手机号
ID_CARD_PATTERN = re.compile(r'\d{17}[\dXx]|\d{15}')  # 身份证
BANK_CARD_PATTERN = re.compile(r'\d{16,19}')  # 银行卡

class ContentAuditor:
    """内容安全审计器：前置审核（拦截违规输入）、后置审核（拦截违规输出）"""
    
    def __init__(self, offline_mode: bool = False):
        self.offline_mode = offline_mode  # 离线模式：仅本地敏感词检测，不调用云端接口
    
    def audit_input(self, content: str) -> Tuple[bool, str]:
        """
        输入内容审核（指令提交时）
        :param content: 用户输入的指令/文本
        :return: (是否通过, 提示信息)
        """
        if not content:
            return True, "内容为空，无需审核"
        
        # 1. 本地敏感词检测
        matched_words = self._check_sensitive_words(content)
        if matched_words:
            logger.warning(f"输入内容包含敏感词：{matched_words} | 内容：{content}")
            return False, f"输入内容包含违规词汇：{','.join(matched_words)}"
        
        # 2. 离线模式跳过云端审核
        if self.offline_mode:
            logger.info("离线模式，跳过云端内容审核")
            return True, "离线模式审核通过"
        
        # 3. 云端审核（示例：实际项目中对接阿里云/腾讯云内容安全API）
        try:
            # 此处为模拟，实际需替换为真实API调用
            cloud_audit_result = self._mock_cloud_audit(content)
            if not cloud_audit_result:
                logger.warning(f"云端审核未通过：{content}")
                return False, "输入内容不符合规范，请修改后重试"
            
            logger.info("输入内容审核通过")
            return True, "审核通过"
        except Exception as e:
            logger.error(f"云端审核异常，降级为本地审核：{str(e)}")
            return True, "云端审核异常，本地审核通过"
    
    def audit_output(self, content: str) -> Tuple[bool, str]:
        """
        输出内容审核（AI返回结果时）
        :param content: AI生成的输出内容
        :return: (是否通过, 提示信息)
        """
        if not content:
            return True, "内容为空，无需审核"
        
        # 仅做本地敏感词检测（输出审核更宽松）
        matched_words = self._check_sensitive_words(content)
        if matched_words:
            logger.warning(f"输出内容包含敏感词：{matched_words} | 内容：{content}")
            return False, "输出内容包含违规词汇，无法返回"
        
        logger.info("输出内容审核通过")
        return True, "审核通过"
    
    def _check_sensitive_words(self, content: str) -> List[str]:
        """
        检测内容中的敏感词
        :return: 匹配到的敏感词列表
        """
        matched = []
        for word in SENSITIVE_WORDS:
            if word in content:
                matched.append(word)
        return matched
    
    def _mock_cloud_audit(self, content: str) -> bool:
        """模拟云端内容审核（实际项目替换为真实API）"""
        # 模拟逻辑：仅拒绝包含"测试违规内容"的文本
        if "测试违规内容" in content:
            return False
        return True

# 全局审计器实例（默认离线模式）
content_auditor = ContentAuditor(offline_mode=True)

# 测试审核功能
if __name__ == "__main__":
    # 测试正常内容
    normal_content = "帮我读取test.txt文件"
    print(content_auditor.audit_input(normal_content))  # 应返回 (True, ...)
    
    # 测试敏感内容
    sensitive_content = "包含rm -rf的恶意指令"
    print(content_auditor.audit_input(sensitive_content))  # 应返回 (False, ...)