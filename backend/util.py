import asyncio

import aiohttp
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)


async def fetch(session, url, as_csv:bool):
    try:
        async with session.get(url, ssl=False) as response:
            if as_csv:
                return await response.json()
            else:
                return {'response': await response.json(), "url": url}
    except Exception as e:
        print(e)
        raise e


async def get_urls(urls: list, as_csv:bool):
    timeout = aiohttp.ClientTimeout(total=30)
    conn = aiohttp.TCPConnector(limit_per_host=20)
    cookie_jar = aiohttp.CookieJar(unsafe=True)
    async with aiohttp.ClientSession(trust_env=True, headers={}, timeout=timeout, connector=conn,
                                     cookie_jar=cookie_jar) as session:
        tasks = []
        for url in urls:
            task = asyncio.create_task(fetch(session, url, as_csv))
            tasks.append(task)
        res = await asyncio.gather(*tasks)
    return res
