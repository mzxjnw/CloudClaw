from typing import Dict, Type
from backend.modules.im.schemas import IMMessage, IMChannelType, IMResponse, IMMessageStatus
from backend.modules.im.adapters.wechat_work import WechatWorkAdapter
from backend.modules.im.adapters.dingtalk import DingTalkAdapter
from backend.modules.im.adapters.feishu import FeishuAdapter
from backend.core.agent.executor import AgentExecutor
from backend.security.content_audit import content_auditor
from backend.infrastructure.logger import logger

# IM适配器映射：渠道类型 -> 适配器类
ADAPTER_MAP: Dict[IMChannelType, Type] = {
    IMChannelType.WECHAT_WORK: WechatWorkAdapter,
    IMChannelType.DINGTALK: DingTalkAdapter,
    IMChannelType.FEISHU: FeishuAdapter
}

# 各渠道适配器配置（示例，实际从数据库读取）
ADAPTER_CONFIG = {
    IMChannelType.WECHAT_WORK: {"app_id": "your_wechat_app_id", "app_secret": "your_wechat_app_secret"},
    IMChannelType.DINGTALK: {"app_key": "your_ding_app_key", "app_secret": "your_ding_app_secret"},
    IMChannelType.FEISHU: {"app_id": "your_feishu_app_id", "app_secret": "your_feishu_app_secret"}
}

class IMMessageProcessor:
    """IM消息处理器：统一接收、解析、审核、处理、回复所有渠道的IM消息"""
    
    def __init__(self):
        # 初始化各渠道适配器实例
        self.adapters = {
            channel_type: adapter_class(**ADAPTER_CONFIG[channel_type])
            for channel_type, adapter_class in ADAPTER_MAP.items()
        }
        # 初始化Agent执行器（处理用户指令）
        self.agent_executor = AgentExecutor()

    def get_adapter(self, channel_type: IMChannelType):
        """获取指定渠道的适配器"""
        adapter = self.adapters.get(channel_type)
        if not adapter:
            raise ValueError(f"不支持的IM渠道类型：{channel_type}")
        return adapter

    async def process(self, channel_type: str, raw_data: dict) -> IMResponse:
        """
        处理IM消息的核心流程
        :param channel_type: 渠道类型字符串（wechat_work/dingtalk/feishu）
        :param raw_data: 渠道原始消息数据
        :return: 回复结果
        """
        try:
            # 1. 转换渠道类型并获取适配器
            channel_enum = IMChannelType(channel_type)
            adapter = self.get_adapter(channel_enum)
            
            # 2. 解析原始消息为通用模型
            im_message = adapter.parse_raw_message(raw_data)
            logger.info(f"开始处理IM消息：{im_message.message_id} | 渠道：{channel_type}")
            
            # 3. 内容安全审核（拦截违规输入）
            audit_pass, audit_msg = content_auditor.audit_input(im_message.content)
            if not audit_pass:
                logger.warning(f"IM消息审核失败：{im_message.message_id} | 原因：{audit_msg}")
                im_message.status = IMMessageStatus.FAILED
                im_message.error_msg = audit_msg
                # 回复审核失败提示
                return await adapter.send_response(im_message, f"指令不符合规范：{audit_msg}")
            
            # 4. 调用Agent处理用户指令（核心逻辑）
            im_message.status = IMMessageStatus.PROCESSING
            agent_result = await self.agent_executor.execute(im_message.content)
            
            # 5. 审核Agent输出内容
            output_audit_pass, output_audit_msg = content_auditor.audit_output(agent_result)
            if not output_audit_pass:
                logger.warning(f"Agent输出审核失败：{im_message.message_id} | 原因：{output_audit_msg}")
                im_message.status = IMMessageStatus.FAILED
                im_message.error_msg = output_audit_msg
                return await adapter.send_response(im_message, "处理结果不符合规范，无法返回")
            
            # 6. 发送回复
            im_message.status = IMMessageStatus.SUCCESS
            return await adapter.send_response(im_message, agent_result)
        
        except Exception as e:
            logger.error(f"处理IM消息异常：{str(e)} | 渠道：{channel_type}")
            # 构造错误回复
            error_msg = f"处理失败：{str(e)}"
            # 尝试获取消息ID（失败时可能为空）
            message_id = raw_data.get("MsgId", raw_data.get("msgId", "unknown"))
            return IMResponse(
                message_id=message_id,
                content=error_msg,
                success=False
            )

# 全局IM消息处理器实例
im_processor = IMMessageProcessor()