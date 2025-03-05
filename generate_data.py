import time
import uuid

from models import ChatCompletionRequest, ChatCompletionResponse
from models.openai_chat.chat_completion import Choice
from models.openai_chat.chat_completion_message import ChatCompletionMessage
from config import config

MODEL_NAME = config.MODEL_NAME


def generate_data(request: ChatCompletionRequest):
    chunk_id = f"chatcmpl-{uuid.uuid4().hex}"
    return ChatCompletionResponse(
        id=chunk_id,
        model=MODEL_NAME,
        created=int(time.time()),
        object="chat.completion",
        choices=[Choice(
            finish_reason="stop",
            index=0,
            message=ChatCompletionMessage(
                content="Hello, how are you?",
                role="assistant",
            )
        )]
    ).model_dump()
