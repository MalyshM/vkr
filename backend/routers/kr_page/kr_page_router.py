import time
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException

from logger import LOGGER
from models import connect_db_data
from redis import process_href, save_resp_and_return_it
from routers.util_funcs import get_teams_for_user_private_without_lect, get_teams_for_param_private_without_lect
from routers.util.util_router import get_all_teachers, get_all_specialities

kr_page_router = APIRouter(tags=["kr page"])


@kr_page_router.get('/api/kr_analyse_simple', name='Plot:plot', status_code=status.HTTP_200_OK,
                    description=
                    """
                            Получает token: str, type: int, kr: str,
                            Returns:
                                Словарь с ключами(преподаватели/аправления/команды)
                            \n
                            {
                              "Трефилин Иван Андреевич": [
                                12,
                                0,
                                14.43,
                                3,
                                6.83,
                                12.3,
                                2,
                    """)
async def kr_analyse_simple(token: str, type_group_by: int, kr: str,
                            db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    teams = await get_teams_for_user_private_without_lect(token, db)
    teams_true = ', '.join([f"'{team['id']}'" for team in teams])
    href = f"kr_analyse_simple-{token}-{type_group_by}-{kr}"
    LOGGER.info(f"{href} start")
    match type_group_by:
        case 0:
            fill_query_str = '(select t.name from team t where t.id = l.team_id)'
            fill_query_str2 = 'group by l.team_id'
        case 1:
            fill_query_str = '(select s.speciality from stud s where s.id = l.stud_id) as speciality'
            fill_query_str2 = 'group by speciality'
        case 2:
            fill_query_str = '(select t.name from teacher t where t.id = l.teacher_id) as teacher_name'
            fill_query_str2 = 'group by teacher_name'
        case _:
            e = HTTPException(status_code=status.HTTP_409_CONFLICT,
                              detail="Неправильно выбран тип 0 - Группировка по командам, 1 - " +
                                     "Группировка по направлениям, 2 - Группировка по преподавателям")
            LOGGER.warning(f"{href} warning {e.detail}")
            raise e
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
        res = await db.execute(f"""
            SELECT
                ARRAY_AGG(l.test) AS test_mark_list,
                {fill_query_str}
            FROM
                lesson l
            WHERE
                l.team_id IN ({teams_true})
                and l.name = '{kr}'
            {fill_query_str2}
        """)
        result = res.fetchall()
        return await save_resp_and_return_it(result, href, start_time)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e


@kr_page_router.get('/api/kr_analyse_with_filters', name='Plot:plot', status_code=status.HTTP_200_OK,
                    description=
                    """
                            Получает token: str, kr: str, type:int, teacher: Optional[str] = None, speciality: Optional[str] = None,
                                          team: Optional[str] = None,
                            Returns:
                                Словарь с ключами(преподаватели/аправления/команды) и любые их сочетания(проверь чтоб понять)
                            \n
                            {
                              "Трефилин Иван Андреевич": [
                                12,
                                0,
                                14.43,
                                3,
                                6.83,
                                12.3,
                                2,
                    """)
async def kr_analyse_with_filters(token: str, kr: str, type_select: int, teacher: Optional[str] = None,
                                  speciality: Optional[str] = None, team: Optional[str] = None,
                                  db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    if team is not None:
        teams_true = ', '.join([team for team in team.split(',')])
    elif teacher is not None:
        teacher_arr = teacher.split(',')
        teams = await get_teams_for_param_private_without_lect(teacher_arr=teacher_arr, db=db)
        teams_true = ', '.join([f"'{team['id']}'" for team in teams])
    else:
        teams = await get_teams_for_user_private_without_lect(token, db)
        teams_true = ', '.join([f"'{team['id']}'" for team in teams])
    if speciality is None:
        specialities = await get_all_specialities(token, db)
        specialities = ', '.join([f"'{speciality['speciality']}'" for speciality in specialities])
    else:
        specialities = speciality.split(',')
        specialities = ', '.join([f"'{speciality}'" for speciality in specialities])
    team_query = ''
    teacher_query = ''
    speciality_query = ''
    href = f"kr_analyse_with_filters-{token}-{kr}-{type_select}-{teacher}-{speciality}-{team}"
    LOGGER.info(f"{href} start")
    match type_select:
        case 0:
            team_query = 't1.name as team_name'
            group_by_query = 'group by team_name'
        case 1:
            teacher_query = 't.name as teacher_name'
            group_by_query = 'group by teacher_name'
        case 2:
            speciality_query = 's.speciality as speciality'
            group_by_query = 'group by speciality'
        case 3:
            team_query = 't1.name as team_name'
            teacher_query = 't.name as teacher_name,'
            group_by_query = 'group by teacher_name,team_name'
        case 4:
            team_query = 't1.name as team_name,'
            speciality_query = 's.speciality as speciality'
            group_by_query = 'group by speciality,team_name'
        case 5:
            teacher_query = 't.name as teacher_name,'
            speciality_query = 's.speciality as speciality'
            group_by_query = 'group by speciality,teacher_name'
        case 6:
            team_query = 't1.name as team_name,'
            teacher_query = 't.name as teacher_name,'
            speciality_query = 's.speciality as speciality'
            group_by_query = 'group by speciality,teacher_name,team_name'
        case _:
            e = HTTPException(status_code=status.HTTP_409_CONFLICT,
                              detail="Неправильно выбран тип(всего их 0,1,2,3,4,5,6)")
            LOGGER.warning(f"{href} warning {e.detail}")
            raise e
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
        res = await db.execute(f"""
            SELECT
                ARRAY_AGG(l.test) AS test_mark_list,
                {teacher_query}
                {team_query}
                {speciality_query}
            FROM
                lesson l
            inner join teacher t on t.id = l.teacher_id
            inner join team t1 on t1.id = l.team_id
            inner join stud s on s.id = l.stud_id
            WHERE
                l.name = '{kr}'
                and l.team_id IN ({teams_true})
                and s.speciality IN ({specialities})
            {group_by_query}
            """)
        result = res.fetchall()
        return await save_resp_and_return_it(result, href, start_time)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e
