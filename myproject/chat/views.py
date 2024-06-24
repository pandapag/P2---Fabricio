from django.http import JsonResponse
import redis.asyncio as redis
from django.views import View
import json
from dotenv import load_dotenv
import os

load_dotenv()

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT'))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

class ChatHistoryView(View):
    async def get(self, request):
        redis_conn = await redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            decode_responses=True
        )
        messages = await redis_conn.lrange("chat_messages", 0, -1)
        await redis_conn.close()
        return JsonResponse([json.loads(message) for message in messages], safe=False)