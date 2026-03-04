import json
from typing import Dict, Any
from backend.modules.im.schemas import IMMessage, IMChannelType, IMResponse, IMMessageStatus
from backend.infrastructure.logger import logger

class FeishuAdapter:
    """飞书适配器：将飞书原始消息转换为通用IM模型，处理回复"""
    
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.channel_type = IMChannelType.FEISHU

    def parse_raw_message(self, raw_data: Dict[str, Any]) -> IMMessage:
        """
        解析飞书原始消息为通用IMMessage模型
        :param raw_data: 飞书Webhook推送的原始JSON数据
        :return: 通用IM消息模型
        """
        try:
            # 飞书消息结构示例（实际以官方文档为准）
            msg_content = raw_data.get("message", {}).get("content", "{}")
            msg_content_dict = json.loads(msg_content)
            message_id = raw_data.get("message", {}).get("message_id", "")
            sender_id = raw_data.get("sender", {}).get("sender_id", {}).get("open_id", "")
            chat_id = raw_data.get("message", {}).get("chat_id", "")
            content = msg_content_dict.get("text", "").strip()
            
            # 过滤@机器人的内容（飞书@格式：<at id=all></at> 或 @机器人名字）
            content = content.replace("<at id=all></at>", "").strip()
            if "@" in content:
                content = content.split(" ", 1)[-1] if " " in content else ""
            
            logger.info(f"解析飞书消息：{message_id} | 发送者：{sender_id} | 内容：{content}")
            
            return IMMessage(
                message_id=message_id,
                channel_type=self.channel_type,
                sender_id=sender_id,
                chat_id=chat_id,
                content=content,
                raw_data=raw_data
            )
        except Exception as e:
            logger.error(f"解析飞书消息失败：{str(e)} | 原始数据：{raw_data}")
            raise Exception(f"飞书消息解析失败：{str(e)}")

    async def send_response(self, message: IMMessage, content: str) -> IMResponse:
        """
        发送回复到飞书
        :param message: 原始IM消息
        :param content: 回复内容
        :return: 回复结果
        """
        try:
            # 模拟调用飞书API发送消息（实际需替换为真实API调用）
            logger.info(f"发送飞书回复：{message.message_id} | 内容：{content}")
            
            # 此处为模拟，实际需调用飞书消息发送接口
            send_success = True
            
            return IMResponse(
                message_id=message.message_id,
                content=content,
                success=send_success
            )
        except Exception as e:
            logger.error(f"发送飞书回复失败：{str(e)} | 消息ID：{message.message_id}")
            return IMResponse(
                message_id=message.message_id,
                content=content,
                success=False
            )