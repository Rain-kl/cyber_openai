import json
import time
import uuid

from models import ChatCompletionRequest, ChatCompletionChunkResponse
from models.openai_chat.chat_completion_chunk import Choice, ChoiceDelta

from config import config

MODEL_NAME = config.MODEL_NAME


def start_chunk(chunk_id):
    return ChatCompletionChunkResponse(
        id=chunk_id,
        choices=[Choice(
            delta=ChoiceDelta(
                role="assistant",
            ),
            index=0,
        )],
        created=int(time.time()),
        model=MODEL_NAME,
        object="chat.completion.chunk",
    ).model_dump()


def final_chunk(chunk_id):
    return ChatCompletionChunkResponse(
        id=chunk_id,
        choices=[Choice(
            delta=ChoiceDelta(),
            index=0,
            finish_reason="stop",
        )],
        created=int(time.time()),
        model=MODEL_NAME,
        object="chat.completion.chunk",
    ).model_dump()


def generate_stream_data(request: ChatCompletionRequest):
    chunk_id = f"chatcmpl-{uuid.uuid4().hex}"
    yield f"data: {json.dumps(start_chunk(chunk_id))}\n\n"
    lines = "Hello, how are you?", "I'm fine, thank you."
    for i, line in enumerate(lines):
        chunk=ChatCompletionChunkResponse(
            id=chunk_id,
            choices=[Choice(
                delta=ChoiceDelta(
                    content=line,
                ),
                index=0,
            )],
            created=int(time.time()),
            model=MODEL_NAME,
            object="chat.completion.chunk",
        ).model_dump()

        yield f"data: {json.dumps(chunk)}\n\n"
        time.sleep(0.5)

    yield f"data: {json.dumps(final_chunk(chunk_id))}\n\n"
    yield "data: [DONE]\n\n"
