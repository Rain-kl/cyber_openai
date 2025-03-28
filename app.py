import asyncio
import json
import time

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
from loguru import logger

from config import config
from models import ChatCompletionRequest
from models.ChatCompletionRequest import ExtraHeaders
from websocket_client import client

app = FastAPI()

MODEL_NAME = config.MODEL_NAME
WAIT_TIMEOUT = 50


@app.post("/v1/chat/completions")
async def stream_data(request: Request, completion_request: ChatCompletionRequest):
    authorization = request.headers.get("authorization").replace("Bearer ", "")
    completion_request.extra_headers = ExtraHeaders(authorization=authorization)
    logger.info("start")
    await client.connect(f"ws://127.0.0.1:6898/{authorization}")
    await client.send_message(completion_request)

    async def get_response_stream():
        try:
            while True:
                try:
                    # Add wait_for_timeout-second timeout for receive_message
                    response = await asyncio.wait_for(client.receive_message(), timeout=WAIT_TIMEOUT)

                    if not response.startswith("data:"):
                        raise ValueError("Invalid response format")
                    else:
                        yield response
                        if response.strip() == "data: [DONE]":
                            break
                except asyncio.TimeoutError:
                    # Format error using OpenAI error format
                    error_response = {
                        "error": {
                            "message": f"Request timed out after waiting for {WAIT_TIMEOUT} seconds",
                            "type": "timeout_error",
                            "code": "timeout_error"
                        }
                    }
                    yield f"data: {json.dumps(error_response)}\n\n"
                    yield "data: [DONE]\n\n"
                    break
        except Exception as e:
            logger.error(f"Error in stream: {str(e)}")
            error_response = {
                "error": {
                    "message": f"An error occurred: {str(e)}",
                    "type": "server_error",
                    "code": "server_error"
                }
            }
            yield f"data: {json.dumps(error_response)}\n\n"
            yield "data: [DONE]\n\n"
            client.close()

    return StreamingResponse(get_response_stream(), media_type="text/event-stream")


@app.get("/v1/models")
async def list_models():
    """
    返回可用模型列表
    """
    current_time = int(time.time())
    models = [
        {"id": MODEL_NAME, "object": "model", "created": current_time - 100000,
         "owned_by": "ryan"},
    ]

    response = {
        "object": "list",
        "data": models
    }
    return JSONResponse(content=response)


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8001, reload=True)
