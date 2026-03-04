from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, Dict, Any
from datetime import datetime

class IMChannelType(str, Enum):
    """IM渠道类型枚举"""
    WECHAT_WORK = "wechat_work"  # 企业微信
    DINGTALK = "dingtalk"        # 钉钉
    FEISHU = "feishu"            # 飞书

class IMMessageStatus(str, Enum):
    """IM消息状态枚举"""
    PENDING = "pending"    # 待处理
    PROCESSING = "processing"  # 处理中
    SUCCESS = "success"    # 处理成功
    FAILED = "failed"      # 处理失败

class IMMessage(BaseModel):
    """IM消息通用模型（所有渠道消息都转换为这个格式）"""
    message_id: str = Field(..., description="消息唯一ID")
    channel_type: IMChannelType = Field(..., description="IM渠道类型")
    sender_id: str = Field(..., description="发送者ID（如企微用户ID）")
    chat_id: str = Field(..., description="会话ID（群/单聊）")
    content: str = Field(..., description="消息文本内容")
    create_time: datetime = Field(default_factory=datetime.now, description="消息创建时间")
    status: IMMessageStatus = Field(default=IMMessageStatus.PENDING, description="消息处理状态")
    error_msg: Optional[str] = Field(None, description="处理失败时的错误信息")
    raw_data: Optional[Dict[str, Any]] = Field(None, description="渠道原始消息数据（保留备用）")

class IMResponse(BaseModel):
    """IM消息回复模型"""
    message_id: str = Field(..., description="对应原消息ID")
    content: str = Field(..., description="回复内容")
    send_time: datetime = Field(default_factory=datetime.now, description="回复发送时间")
    success: bool = Field(..., description="是否发送成功")