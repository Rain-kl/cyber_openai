from openai import OpenAI

client=OpenAI(
    api_key="sk-lVNgkL4WbC4uJc3h5sWcUzKPdo3SrsOEBTjfG50qovzAM687",
    base_url="https://xapi.coir.us.kg/v1"
)

# 1. 创建一个模型
model = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a chatbot."},
        {"role": "user", "content": "你好"},
    ],
    stream=True
)

for msg in model:
    print(msg.model_dump())