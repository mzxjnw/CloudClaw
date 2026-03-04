import json
from typing import Dict, Any
from backend.modules.im.schemas import IMMessage, IMChannelType, IMResponse, IMMessageStatus
from backend.infrastructure.logger import logger

class DingTalkAdapter:
    """钉钉适配器：将钉钉原始消息转换为通用IM模型，处理回复"""
    
    def __init__(self, app_key: str, app_secret: str):
        self.app_key = app_key
        self.app_secret = app_secret
        self.channel_type = IMChannelType.DINGTALK

    def parse_raw_message(self, raw_data: Dict[str, Any]) -> IMMessage:
        """
        解析钉钉原始消息为通用IMMessage模型
        :param raw_data: 钉钉Webhook推送的原始JSON数据
        :return: 通用IM消息模型
        """
        try:
            # 钉钉消息结构示例（实际以官方文档为准）
            msg_body = raw_data.get("text", {})
            message_id = raw_data.get("msgId", "")
            sender_id = raw_data.get("senderId", "")
            chat_id = raw_data.get("chatId", "")
            content = msg_body.get("content", "").strip()
            
            # 过滤@机器人的内容（钉钉@格式：@机器人昵称 内容）
            if "@" in content:
                content = content.split(" ", 1)[-1] if " " in content else ""
            
            logger.info(f"解析钉钉消息：{message_id} | 发送者：{sender_id} | 内容：{content}")
            
            return IMMessage(
                message_id=message_id,
                channel_type=self.channel_type,
                sender_id=sender_id,
                chat_id=chat_id,
                content=content,
                raw_data=raw_data
            )
        except Exception as e:
            logger.error(f"解析钉钉消息失败：{str(e)} | 原始数据：{raw_data}")
            raise Exception(f"钉钉消息解析失败：{str(e)}")

    async def send_response(self, message: IMMessage, content: str) -> IMResponse:
        """
        发送回复到钉钉
        :param message: 原始IM消息
        :param content: 回复内容
        :return: 回复结果
        """
        try:
            # 模拟调用钉钉API发送消息（实际需替换为真实API调用）
            logger.info(f"发送钉钉回复：{message.message_id} | 内容：{content}")
            
            # 此处为模拟，实际需调用钉钉消息发送接口
            send_success = True
            
            return IMResponse(
                message_id=message.message_id,
                content=content,
                success=send_success
            )
        except Exception as e:
            logger.error(f"发送钉钉回复失败：{str(e)} | 消息ID：{message.message_id}")
            return IMResponse(
                message_id=message.message_id,
                content=content,
                success=False
            )