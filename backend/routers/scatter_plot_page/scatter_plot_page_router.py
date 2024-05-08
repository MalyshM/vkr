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

scatter_plot_page_router = APIRouter(tags=["scatter plot page"])


@scatter_plot_page_router.get('/api/stud_scatter_plot', name='Plot:plot', status_code=status.HTTP_200_OK,
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
async def stud_scatter_plot(token: str, type_group_by: int,teacher_list: Optional[str] = None,
                                  speciality_list: Optional[str] = None, team_list: Optional[str] = None,
                            db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    teams = await get_teams_for_user_private_without_lect(token, db)
    if teacher_list is not None:
        teacher_arr = teacher_list.split(',')
        teams = await get_teams_for_param_private_without_lect(teacher_arr=teacher_arr, db=db)
    teams_true = ', '.join([f"'{team['id']}'" for team in teams])
    if speciality_list is not None:
        speciality_list = speciality_list.split(',')
        speciality_list = ', '.join([f"'{speciality}'" for speciality in speciality_list])
        speciality_cond = f"AND s.speciality IN ({speciality_list})"
    else:
        speciality_cond = ""
    href = f"stud_scatter_plot-{token}-{type_group_by}-{teacher_list}-{speciality_list}-{team_list}"
    LOGGER.info(f"{href} start")
    match type_group_by:
        case 0:
            fill_query_str = 'sub.team_id'
            fill_query_str2 = 'group by sub.team_id,'
        case 1:
            fill_query_str = 'sub.speciality'
            fill_query_str2 = 'group by sub.speciality,'
        case 2:
            fill_query_str = 'sub.teacher_id'
            fill_query_str2 = 'group by sub.teacher_id,'
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
                json_agg(
                    json_build_object(
                        'Успеваемость', sub.Успеваемость, 
                        'Посещаемость', sub.Посещаемость, 
                        'stud_id', sub.stud_id
                    )
                ) AS result1,
                {fill_query_str},
                sub.name
            FROM (
                SELECT 
                    ROUND((
                        SUM(l.mark_for_work) OVER (
                            PARTITION BY l.stud_id 
                            ORDER BY l.id 
                            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                        ) +
                        SUM(l.test) OVER (
                            PARTITION BY l.stud_id 
                            ORDER BY l.id 
                            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                        )
                    )::DECIMAL, 2) AS Успеваемость,
                    ROUND((
                        COUNT(l.id) FILTER (WHERE l.arrival = 'П') OVER (
                            PARTITION BY l.stud_id 
                            ORDER BY l.id 
                            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                        ) * 100 /
                        COUNT(l.id) OVER (
                            PARTITION BY l.stud_id 
                            ORDER BY l.id 
                            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                        )
                    )::DECIMAL, 2) AS Посещаемость,
                    l.name,
                    l.stud_id,
                    l.team_id,
                    l.teacher_id,
                    (SELECT s.speciality FROM stud s WHERE s.id = l.stud_id)
                FROM lesson l
                WHERE l.team_id IN ({teams_true})
                {speciality_cond}
            ) AS sub
            WHERE sub.name IN (
                'Организация функций30', 'Коллекции. Работа с файлами20', 'Управляющие конструкции50', 'Аттестация00'
            )
            {fill_query_str2}
            sub.name;
        """)
        result = res.fetchall()
        return await save_resp_and_return_it(result, href, start_time)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e


@scatter_plot_page_router.get('/api/median_scatter_plot', name='Plot:plot', status_code=status.HTTP_200_OK,
                    description=
                    """
                            Получает token: str, type: int, kr: str,
                            Returns:
                                Словарь с ключами(преподаватели/аправления/команды)
                            \n
                            {
                              "Трефилин Иван Андреевич": [
                              
                              ]
                    """)
async def median_scatter_plot(token: str, type_group_by: int,teacher_list: Optional[str] = None,
                                  speciality_list: Optional[str] = None, team_list: Optional[str] = None,
                            db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    teams = await get_teams_for_user_private_without_lect(token, db)
    if teacher_list is not None:
        teacher_arr = teacher_list.split(',')
        teams = await get_teams_for_param_private_without_lect(teacher_arr=teacher_arr, db=db)
    teams_true = ', '.join([f"'{team['id']}'" for team in teams])
    if speciality_list is not None:
        speciality_list = speciality_list.split(',')
        speciality_list = ', '.join([f"'{speciality}'" for speciality in speciality_list])
        speciality_cond = f"AND s.speciality IN ({speciality_list})"
    else:
        speciality_cond = ""
    href = f"stud_scatter_plot-{token}-{type_group_by}-{teacher_list}-{speciality_list}-{team_list}"
    LOGGER.info(f"{href} start")
    match type_group_by:
        case 0:
            fill_query_str = 'sub.team_id'
            fill_query_str2 = 'group by sub.team_id,'
        case 1:
            fill_query_str = 'sub.speciality'
            fill_query_str2 = 'group by sub.speciality,'
        case 2:
            fill_query_str = 'sub.teacher_id'
            fill_query_str2 = 'group by sub.teacher_id,'
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
                json_agg(
                    json_build_object(
                        'Медианная_посещаемость', percentile_cont(0.5) 
                        WITHIN GROUP (ORDER BY sub.Посещаемость) 
                        OVER (PARTITION BY {fill_query_str}),
                        'Медианная_успеваемость', percentile_cont(0.5) 
                        WITHIN GROUP (ORDER BY sub.Успеваемость)
                        OVER (PARTITION BY {fill_query_str}),
                    )
                ) AS result1,
                {fill_query_str},
                sub.name
            FROM (
                SELECT 
                    ROUND((
                        SUM(l.mark_for_work) OVER (
                            PARTITION BY l.stud_id 
                            ORDER BY l.id 
                            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                        ) +
                        SUM(l.test) OVER (
                            PARTITION BY l.stud_id 
                            ORDER BY l.id 
                            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                        )
                    )::DECIMAL, 2) AS Успеваемость,
                    ROUND((
                        COUNT(l.id) FILTER (WHERE l.arrival = 'П') OVER (
                            PARTITION BY l.stud_id 
                            ORDER BY l.id 
                            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                        ) * 100 /
                        COUNT(l.id) OVER (
                            PARTITION BY l.stud_id 
                            ORDER BY l.id 
                            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                        )
                    )::DECIMAL, 2) AS Посещаемость,
                    l.name,
                    l.stud_id,
                    l.team_id,
                    l.teacher_id,
                    (SELECT s.speciality FROM stud s WHERE s.id = l.stud_id)
                FROM lesson l
                WHERE l.team_id IN ({teams_true})
                {speciality_cond}
            ) AS sub
            WHERE sub.name IN (
                'Организация функций30', 'Коллекции. Работа с файлами20', 'Управляющие конструкции50', 'Аттестация00'
            )
            {fill_query_str2}
            sub.name;
        """)
        result = res.fetchall()
        return await save_resp_and_return_it(result, href, start_time)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e

