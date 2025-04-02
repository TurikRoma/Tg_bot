from openai import AsyncOpenAI
import httpx
import os

client = AsyncOpenAI(
    api_key=os.getenv("API_KEY"),
    base_url="https://api.proxyapi.ru/anthropic/v1",
)

BASE_URL = "https://api.proxyapi.ru/anthropic/v1"
API_KEY = "sk-bhGeAfyiUE9WPl4BpjrGfO1rEurj8bn7"

async def gpt(question,context):

    async with httpx.AsyncClient(timeout=60.0) as client:
        print(context[1])
        response = await client.post(
            f"{BASE_URL}/messages",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "system": context[0],
                "model": "claude-3-5-haiku-20241022",  # Убедитесь, что указываете правильную модель
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": context[1] + question}],
            }
        )

    
        print(response.json())

        response = response.json()

        response_for_user = response['content'][0]['text'].split('\n\n')
        response_for_bd = response['content'][0]['text']

        return [response_for_user, response_for_bd]
    

async def mental_analysis_gpt(context):

    async with httpx.AsyncClient(timeout=60.0) as client:
        print(context[1])
        response = await client.post(
            f"{BASE_URL}/messages",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                # "system": context,
                "model": "claude-3-5-haiku-20241022",  # Убедитесь, что указываете правильную модель
                "max_tokens": 4000,
                "messages": [{"role": "user", "content": context}],
            }
        )

    
        print(response.json())

        response = response.json()

        return response['content'][0]['text']




