import time

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException
from logger import LOGGER
from main import *
from models import connect_db_data
from redis import process_href, save_resp_and_return_it
from routers.util_funcs import get_current_user_dev

util_router = APIRouter(tags=["Util"])


@util_router.get('/api/get_router_paths', name='Util:Util', status_code=status.HTTP_200_OK,
                 description=
                 """
                         Получает id_team: int, id_stud: int
                         Returns:
                             response_list = []
                             response_list.append({'name': row['name'], 'cum_sum': cum_sum[-1], 'counter': row['counter'], 'isTest': temp})
                         \n
                         [
                           {
                             "name": "Основные принципы организации Языка Python. Базовые элементы программирования и типы данных",
                             "cum_sum": 2,
                             "counter": 1,
                             "isTest": false
                           },
                           {
                             "name": "Основные принципы организации Языка Python. Базовые элементы программирования и типы данных1",
                             "cum_sum": 4,
                             "counter": 2,
                             "isTest": false
                           },
                 """)
async def get_router_paths():
    start_time = time.time()
    href = "get_router_paths"
    LOGGER.info(f"{href} start")
    try:
        router_list = [{"path": route.path, "name": route.name} for route in app.routes]
        resp = []
        for item in router_list:
            if "Registration" not in item['name'] and "User" not in item['name'] \
                    and "Team" not in item['name'] and "Stud" not in item['name'] \
                    and "Reporting system" not in item['name'] and "Util" not in item['name']:
                resp.append(item['path'])
        LOGGER.info(f"{href} finish {(time.time() - start_time)}")
        return resp
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e


@util_router.get('/api/get_all_specialities', name='Util:get_all_specialities', status_code=status.HTTP_200_OK,
                 description=
                 """
                         Получает token: str
                         Returns:
                             специальности 
                         \n
                         [
                           {
                             "speciality": "43.03.02 Туризм"
                           },
                           {
                             "speciality": "01.03.03 Механика и математическое моделирование"
                           },
                           {
                             "speciality": "35.03.10 Ландшафтная архитектура"
                           },
                 """)
async def get_all_specialities(token: str, db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    user = await get_current_user_dev(token)
    user_fio = user.fio
    href = f"get_all_specialities-{token}"
    LOGGER.info(f"{href} start")
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
        if user.iscurator or user.isadmin:
            response = await db.execute("""
                    select distinct
                        s.speciality 
                    from
                        stud s 
                """)
        elif user.isteacher:
            response = await db.execute(f"""
                    select distinct
                        s.speciality 
                    from
                        stud s
                    where
                        s.id in (
                        select
                            distinct l.stud_id
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


@util_router.get('/api/get_all_specialities_by_teacher_arr', name='Util:get_all_specialities_by_teacher_arr', status_code=status.HTTP_200_OK,
                 description=
                 """
                         Получает token: str
                         Returns:
                             специальности 
                         \n
                         [
                           {
                             "speciality": "43.03.02 Туризм"
                           },
                           {
                             "speciality": "01.03.03 Механика и математическое моделирование"
                           },
                           {
                             "speciality": "35.03.10 Ландшафтная архитектура"
                           },
                 """)
async def get_all_specialities_by_teacher_arr(token: str, teacher_list: str, db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    user = await get_current_user_dev(token)
    href = f"get_all_specialities_by_teacher_arr-{token}-{teacher_list}"
    LOGGER.info(f"{href} start")
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
        if user.iscurator or user.isadmin:
            res = await db.execute(f"""
                                select distinct
                                    s.speciality 
                                from
                                    stud s
                                where
                                    s.id in (
                                    select
                                        distinct l.stud_id
                                    from
                                        lesson l
                                    where
                                        l.teacher_id in (
                                        select
                                            distinct t.id
                                        from
                                            teacher t
                                        where
                                            t.name = ANY(ARRAY{teacher_list.split(',')})))
                            """)
            result = res.fetchall()
            return await save_resp_and_return_it(result, href, start_time)
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="ВАМ ЗАПРЕЩАЕТСЯ ВХОД В СЕКРЕТНЫЙ РАЗДЕЛ КОНТРОЛЯ УСПЕВАЕМОСТИ")
    except HTTPException as e:
        LOGGER.error(f"{href} Error {e.detail}")
        raise e
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e

@util_router.get('/api/get_all_kr', name='Util:get_all_kr', status_code=status.HTTP_200_OK, description=
"""
        Returns:
            все кр
        \n
        [
          {
            "name": "Организация функций30"
          },
          {
            "name": "Коллекции. Работа с файлами20"
          },
          {
            "name": "Управляющие конструкции50"
          }
        ]
""")
async def get_all_kr(db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    href = f"get_all_kr"
    LOGGER.info(f"{href} start")
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
        all_users = await db.execute("""
            select distinct 
                l.name
            from
                lesson l
            where
                l.test >= 0.0
        """)
        result = all_users.fetchall()
        return await save_resp_and_return_it(result, href, start_time)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e


@util_router.get('/api/get_all_teachers_unique', name='Util:get_all_teachers', status_code=status.HTTP_200_OK,
                 description=
                 """
                         Получает token: str
                         Returns:
                             Преподаватели
                         \n
                         [
                           {
                             "id": 8,
                             "name": "Березовский Артем Константинович"
                           },
                           {
                             "id": 2,
                             "name": "Трефилин Иван Андреевич"
                           },
                           {
                             "id": 4,
                             "name": "Павлова Елена Александровна"
                           },
                 """)
async def get_all_teachers_unique(token: str, db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    user = await get_current_user_dev(token)
    user_fio = user.fio
    href = f"get_all_teachers_unique-{token}"
    LOGGER.info(f"{href} start")
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
        if user.iscurator or user.isadmin:
            response = await db.execute("""
                    select distinct
                        t.id,
                        t."name"
                    from
                        teacher t
                    where 
                        t.name not ilike '%,%'
                """)
        elif user.isteacher:
            response = await db.execute(f"""
                    select distinct
                        t.id,
                        t."name"
                    from
                        teacher t
                    where
                        t.name = '{user_fio}'
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


@util_router.get('/api/get_all_teachers', name='Util:get_all_teachers', status_code=status.HTTP_200_OK,
                 description=
                 """
                         Получает token: str
                         Returns:
                             Преподаватели
                         \n
                         [
                           {
                             "id": 8,
                             "name": "Березовский Артем Константинович"
                           },
                           {
                             "id": 2,
                             "name": "Трефилин Иван Андреевич"
                           },
                           {
                             "id": 4,
                             "name": "Павлова Елена Александровна"
                           },
                 """)
async def get_all_teachers(token: str, db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    user = await get_current_user_dev(token)
    user_fio = user.fio
    href = f"get_all_teachers-{token}"
    LOGGER.info(f"{href} start")
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
        if user.iscurator or user.isadmin:
            response = await db.execute("""
                        select distinct
                            t.id,
                            t."name"
                        from
                            teacher t
                    """)
        elif user.isteacher:
            response = await db.execute(f"""
                    select distinct
                        t.id,
                        t."name"
                    from
                        teacher t
                    where
                        t.name ilike '%{user_fio}%'
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
