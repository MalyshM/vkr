import json
import aioredis
import asyncio
import time
from decimal import Decimal
from datetime import datetime

from handlers import LOGGER


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


async def process_href(href, start_time) -> list | None:
    try:
        res = await check_href(href)
        print("--- %s seconds ---" % (time.time() - start_time), end=" finish redis\n")
        LOGGER.info(f"{href}--- {(time.time() - start_time)} seconds --- finish redis")
        return res
    except Exception as e:
        print(e)
        LOGGER.warning(f"{href} {e}")
        return None


async def save_resp_and_return_it(result, href, start_time, skip: bool = False) -> list:
    if skip:
        result_dicts = result
    else:
        result_dicts = [row._asdict() for row in result]
    for row_dict in result_dicts:
        for key, value in row_dict.items():
            if isinstance(value, Decimal):
                row_dict[key] = float(value)
            if isinstance(value, datetime):
                row_dict[key] = value.strftime('%Y-%m-%d %H:%M')
    await save_resp(href, result_dicts)
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    LOGGER.info(f"{href} finish {(time.time() - start_time)}")
    return result_dicts


if __name__ == "__main__":
    asyncio.run(main())
