import time

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException
from logger import LOGGER
from models import connect_db_data
from redis import process_href, save_resp_and_return_it
from routers.util_funcs import get_current_user_dev

team_router = APIRouter(tags=["Team"])


@team_router.get('/api/get_teams_for_user', name='Team:get_teams_for_user', status_code=status.HTTP_200_OK,
                 description=
                 """
                         Получает токен
                         Raises:
                             raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                 detail="ВАМ ЗАПРЕЩАЕТСЯ ВХОД В СЕКРЕТНЫЙ РАЗДЕЛ КОНТРОЛЯ УСПЕВАЕМОСТИ")
     
                         Returns:
                             массив Team (Team.id, Team.name)
                         \n
                         [
                           {
                             "id": 17,
                             "name": "ПиОА П-06.02"
                           },
                           {
                             "id": 39,
                             "name": "ПиОА П-07.03"
                           },
                 """)
async def get_teams_for_user(token: str, db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    user = await get_current_user_dev(token)
    user_fio = user.fio
    href = f"get_teams_for_user-{token}"
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


@team_router.get('/api/get_teams_for_user_without_lect', name='Team:get_teams_for_user_without_lect',
                 status_code=status.HTTP_200_OK,
                 description=
                 """
                         Получает токен
                         Raises:
                             raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                 detail="ВАМ ЗАПРЕЩАЕТСЯ ВХОД В СЕКРЕТНЫЙ РАЗДЕЛ КОНТРОЛЯ УСПЕВАЕМОСТИ")
     
                         Returns:
                             массив Team (Team.id, Team.name)
                         \n
                         [
                           {
                             "id": 17,
                             "name": "ПиОА П-06.02"
                           },
                           {
                             "id": 39,
                             "name": "ПиОА П-07.03"
                           },
                 """)
async def get_teams_for_user_without_lect(token: str, db: AsyncSession = Depends(connect_db_data)):
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
