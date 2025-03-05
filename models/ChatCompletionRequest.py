from typing import List, Optional, Dict, Union

from ._model import BaseModel


class ContentMsg(BaseModel):
    type: str
    text: str


# 数据模型
class Message(BaseModel):
    role: str
    content: str | List[ContentMsg]


class ExtraBody(BaseModel):
    FC_flag: bool = False  # 使用function call
    RAG_flag: bool = False  # 强制使用RAG
    MIX_flag: bool = True


class ExtraHeaders(BaseModel):
    authorization: str


class ChatCompletionRequest(BaseModel):
    model: str  # 模型名称
    messages: List[Message]  # 消息列表
    temperature: Optional[float] = 1.0  # 温度
    top_p: Optional[float] = 1.0  # top-p
    n: Optional[int] = 1
    stream: Optional[bool] = False
    stop: Optional[Union[str, List[str]]] = None
    max_tokens: Optional[int] = None
    presence_penalty: Optional[float] = 0
    frequency_penalty: Optional[float] = 0
    logit_bias: Optional[Dict[str, float]] = None
    user: Optional[str] = None
    extra_headers: ExtraHeaders | None = None,
    extra_body: ExtraBody | None = None

    def get_content(self):
        assert len(self.messages) == 1
        return self.messages[0].content
