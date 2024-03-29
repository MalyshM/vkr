import ast

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
    res = ast.literal_eval(cached_response)
    if res is not None:
        await redis.close()
        return res
    else:
        raise


async def save_resp(href: str, resp):
    redis = await connect_to_redis_true()
    await redis.set(str(href), str(resp), ex=3600)


if __name__ == "__main__":
    asyncio.run(main())
