import json
import aioredis
import asyncio


async def connect_to_redis():
    redis = await aioredis.create_redis('redis://localhost', encoding='utf-8')
    return redis


async def main():
    redis = await connect_to_redis()
    print(redis)


async def connect_to_redis_true():
    redis = aioredis.from_url(
        'redis://redis:6379',
        encoding='utf-8',
        decode_responses=True)
    return redis


async def check_href(href: str):
    redis = await connect_to_redis_true()
    cached_response = await redis.get(href)
    if cached_response is not None:
        await redis.close()
        return json.loads(cached_response)
    else:
        raise Exception("Cached response from Redis is None")


async def save_resp(href: str, resp):
    redis = await connect_to_redis_true()
    await redis.set(name=str(href), value=json.dumps(resp), ex=3600)


if __name__ == "__main__":
    asyncio.run(main())
