import asyncio
import time
from datetime import timedelta, datetime

import aiohttp
import jwt
from passlib.context import CryptContext
from starlette import status
from starlette.exceptions import HTTPException
from backend.logger import LOGGER
from backend.models import async_session_users
from backend.redis import process_href, save_resp_and_return_it
from backend.schemas import TokenData

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_teams_for_user_private(token: str, db):
    start_time = time.time()
    user = await get_current_user_dev(token)
    user_fio = user.fio
    href = f"get_teams_for_user_private-{token}"
    LOGGER.info(f"{href} start")
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
        if user.iscurator or user.isadmin:
            response = await db.execute("""
                    select distinct t.id, t.name from team t
                    """)
        elif user.isteacher:
            response = await db.execute(f"""
                        select
                            distinct t.id,
                            t.name
                        from
                            team t
                        where
                            t.id in (
                            select
                                distinct l.team_id
                            from
                                lesson l
                            where
                                l.teacher_id in (
                                select
                                    distinct t.id
                                from
                                    teacher t
                                where
                                    t.name ilike '%{user_fio}%'))
                    """)
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="ВАМ ЗАПРЕЩАЕТСЯ ВХОД В СЕКРЕТНЫЙ РАЗДЕЛ КОНТРОЛЯ УСПЕВАЕМОСТИ")
        result = response.fetchall()
        return await save_resp_and_return_it(result, href, start_time)
    except HTTPException as e:
        LOGGER.error(f"{href} Error {e.detail}")
        raise e
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e


async def get_teams_for_param_private_without_lect(teacher_arr: list, db):
    start_time = time.time()
    href = f"get_teams_for_param_private_without_lect-{teacher_arr}"
    LOGGER.info(f"{href} start")
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
        res = await db.execute(f"""
                            select
                                distinct t.id,
                                t.name
                            from
                                team t
                            where
                                t.id in (
                                select
                                    distinct l.team_id
                                from
                                    lesson l
                                where
                                    l.teacher_id in (
                                    select
                                        distinct t.id
                                    from
                                        teacher t
                                    where
                                        t.name = ANY(ARRAY{teacher_arr}))
                                and t.name not ilike '%л%');
                                    """)
        result = res.fetchall()
        return await save_resp_and_return_it(result, href, start_time)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e


async def get_teams_for_user_private_without_lect(token: str, db):
    start_time = time.time()
    user = await get_current_user_dev(token)
    user_fio = user.fio
    href = f"get_teams_for_user_without_lect-{token}"
    LOGGER.info(f"{href} start")
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
        if user.iscurator or user.isadmin:
            res = await db.execute("""
                        select
                            distinct t.id,
                            t."name"
                        from
                            team t
                        where
                            t."name" not ilike '%л%'
                    """)
        elif user.isteacher:
            res = await db.execute(f"""
                                select
                                    distinct t.id,
                                    t.name
                                from
                                    team t
                                where
                                    t.id in (
                                    select
                                        distinct l.team_id
                                    from
                                        lesson l
                                    where
                                        l.teacher_id in (
                                        select
                                            distinct t.id
                                        from
                                            teacher t
                                        where
                                            t.name ilike '%{user_fio}%'))
                                    and t.name not ilike '%л%'
                                """)
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="ВАМ ЗАПРЕЩАЕТСЯ ВХОД В СЕКРЕТНЫЙ РАЗДЕЛ КОНТРОЛЯ УСПЕВАЕМОСТИ")
        result = res.fetchall()
        return await save_resp_and_return_it(result, href, start_time)
    except HTTPException as e:
        LOGGER.error(f"{href} Error {e.detail}")
        raise e
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    start_time = time.time()
    href = f"create_access_token-{data}-{expires_delta}"
    LOGGER.info(f"{href} start")
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    LOGGER.info(f"{href} finish {(time.time() - start_time)}")
    return encoded_jwt


async def get_current_user_dev(token: str):
    start_time = time.time()
    href = f"get_current_user_dev-{token}"
    LOGGER.info(f"{href} start")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Нерабочий токен",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("username")
            password: str = payload.get("password")
            email: str = payload.get("email")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username, password=password, email=email)

        except:
            raise credentials_exception
        user = await get_user(username=token_data.username, email=token_data.email)
        if user is None:
            raise credentials_exception
        LOGGER.info(f"{href} finish {(time.time() - start_time)}")
        return user
    except HTTPException as e:
        LOGGER.error(f"{href} Error {e.detail}")
        raise e
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e


async def get_user(username, email):
    start_time = time.time()
    href = f"get_user-{username}-{email}"
    LOGGER.info(f"{href} start")
    try:
        async with async_session_users() as db:
            query = await db.execute(f"""
                select
                *
            from users u
            where 
                u.username ='{username}' and
                u.email = '{email}'
                """)
            user = query.one()
            LOGGER.info(f"{href} finish {(time.time() - start_time)}")
            return user
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e


class Hasher:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)


async def fetch(session, url, as_csv: bool):
    try:
        async with session.get(url, ssl=False) as response:
            if as_csv:
                return await response.json()
            else:
                return {'response': await response.json(), "url": url}
    except Exception as e:
        print(e)
        raise e


async def get_urls(urls: list, as_csv: bool):
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
