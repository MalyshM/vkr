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
                                      Получает token: str, type_group_by: int, teacher_list: Optional[str] = None,
                                      speciality_list: Optional[str] = None, team_list: Optional[str] = None
                                      raises:
                                        HTTPException(status_code=status.HTTP_409_CONFLICT,
                                        detail="Неправильно выбран тип 0 - Группировка по командам, 1 - " +
                                        "Группировка по направлениям, 2 - Группировка по преподавателям")
                                      Returns:
                                          Словарь с ключами(преподаватели/аправления/команды)
                                        \n
                                        [
                                          {
                                            "result1": [
                                              {
                                                "Успеваемость": 91,
                                                "Посещаемость": 90,
                                                "stud_id": 299
                                              },
                                              {
                                                "Успеваемость": 77,
                                                "Посещаемость": 95,
                                                "stud_id": 927
                                              }
                                            ],
                                            "team_id": 2, - team_id/spesiclity/teacher_id
                                            "name": "Аттестация00" - название майлстоуна
                                          },
                                        ]
                                  """)
async def stud_scatter_plot(token: str, type_group_by: int, teacher_list: Optional[str] = None,
                            speciality_list: Optional[str] = None, team_list: Optional[str] = None,
                            db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    if team_list is not None:
        teams_true = ', '.join([f"'{team}'" for team in team_list.split(',')])
    elif teacher_list is not None:
        teacher_arr = teacher_list.split(',')
        teams = await get_teams_for_param_private_without_lect(teacher_arr=teacher_arr, db=db)
        teams_true = ', '.join([f"'{team['id']}'" for team in teams])
    else:
        teams = await get_teams_for_user_private_without_lect(token, db)
        teams_true = ', '.join([f"'{team['id']}'" for team in teams])
    if speciality_list is not None:
        speciality_list = speciality_list.split(',')
        speciality_list = ', '.join([f"'{speciality}'" for speciality in speciality_list])
        speciality_cond = f"AND s.speciality IN ({speciality_list})"
        speciality_join = "INNER JOIN stud s on s.id = l.stud_id"
    else:
        speciality_cond = ""
        speciality_join = ""
    href = f"stud_scatter_plot-{token}-{type_group_by}-{teacher_list}-{speciality_list}-{team_list}"
    LOGGER.info(f"{href} start")
    match type_group_by:
        case 0:
            query_field = 'sub.team_id'
            sub_query_field = "(SELECT t.name FROM team t WHERE t.id = l.team_id) AS team_id"
            group_by = 'group by sub.team_id,'
        case 1:
            query_field = 'sub.speciality'
            sub_query_field = "(SELECT s.speciality FROM stud s WHERE s.id = l.stud_id)"
            group_by = 'group by sub.speciality,'
        case 2:
            query_field = 'sub.teacher_id'
            sub_query_field = "(SELECT t.name FROM teacher t WHERE t.id = l.teacher_id) AS teacher_id"
            group_by = 'group by sub.teacher_id,'
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
                        'stud_id', sub.stud_id,
                        'stud_name', sub.stud_name
                    )
                ) AS result1,
                sub.name,
                sub.lesson_counter,
                {query_field}
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
                        ROUND(COUNT(l.id) FILTER (WHERE l.arrival = 'П') OVER (
                            PARTITION BY l.stud_id 
                            ORDER BY l.id 
                            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                        )::DECIMAL, 2)
                    )::DECIMAL, 2) AS Посещаемость,
                    l.name,
                    l.stud_id,
                    (SELECT s.name FROM stud s WHERE s.id = l.stud_id) AS stud_name,
                    COUNT(l.name) OVER (
                            PARTITION BY l.team_id, l.stud_id 
                            ORDER BY l.id 
                            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                        ) as lesson_counter,
                    {sub_query_field}
                FROM lesson l
                {speciality_join}
                WHERE l.team_id IN ({teams_true})
                {speciality_cond}
            ) AS sub
            WHERE sub.name IN (
                'Организация функций30', 'Коллекции. Работа с файлами20', 'Управляющие конструкции50', 'Аттестация00'
            )
            {group_by}
            sub.name, sub.lesson_counter;
        """)
        result = res.fetchall()
        return await save_resp_and_return_it(result, href, start_time)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e


@scatter_plot_page_router.get('/api/scatter_plot_by_section', name='Plot:plot', status_code=status.HTTP_200_OK,
                              description=
                              """
                                      Получает token: str, type_group_by: int, teacher_list: Optional[str] = None,
                                      speciality_list: Optional[str] = None, team_list: Optional[str] = None
                                      raises:
                                        HTTPException(status_code=status.HTTP_409_CONFLICT,
                                        detail="Неправильно выбран тип 0 - Группировка по командам, 1 - " +
                                        "Группировка по направлениям, 2 - Группировка по преподавателям")
                                      Returns:
                                          Словарь с ключами(преподаватели/аправления/команды)
                                        \n
                                        [
                                          {
                                            "Медианная_посещаемость": 86,
                                            "Медианная_успеваемость": 68,
                                            "teacher_id": 2, - team_id/spesiclity/teacher_id
                                            "name": "Аттестация00"
                                          },
                                        ]
                                  """)
async def scatter_plot_by_section(token: str, type_group_by: int, teacher_list: Optional[str] = None,
                                  speciality_list: Optional[str] = None, team_list: Optional[str] = None,
                                  db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    if team_list is not None:
        teams_true = ', '.join([f"'{team}'" for team in team_list.split(',')])
    elif teacher_list is not None:
        teacher_arr = teacher_list.split(',')
        teams = await get_teams_for_param_private_without_lect(teacher_arr=teacher_arr, db=db)
        teams_true = ', '.join([f"'{team['id']}'" for team in teams])
    else:
        teams = await get_teams_for_user_private_without_lect(token, db)
        teams_true = ', '.join([f"'{team['id']}'" for team in teams])
    if speciality_list is not None:
        speciality_list = speciality_list.split(',')
        speciality_list = ', '.join([f"'{speciality}'" for speciality in speciality_list])
        speciality_cond = f"AND s.speciality IN ({speciality_list})"
        speciality_join = "INNER JOIN stud s on s.id = l.stud_id"
    else:
        speciality_cond = ""
        speciality_join = ""
    href = f"scatter_plot_by_section-{token}-{type_group_by}-{teacher_list}-{speciality_list}-{team_list}"
    LOGGER.info(f"{href} start")
    match type_group_by:
        case 0:
            query_field = 'sub.team_id'
            sub_query_field = "(SELECT t.name FROM team t WHERE t.id = l.team_id) AS team_id"
            group_by = 'group by sub.team_id,'
        case 1:
            query_field = 'sub.speciality'
            sub_query_field = "(SELECT s.speciality FROM stud s WHERE s.id = l.stud_id)"
            group_by = 'group by sub.speciality,'
        case 2:
            query_field = 'sub.teacher_id'
            sub_query_field = "(SELECT t.name FROM teacher t WHERE t.id = l.teacher_id) AS teacher_id"
            group_by = 'group by sub.teacher_id,'
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
                PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY sub.Посещаемость) as Медианная_посещаемость,
                PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY sub.Успеваемость) as Медианная_успеваемость,
                sub.name,
                sub.lesson_counter,
                {query_field}
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
                        ROUND(COUNT(l.id) FILTER (WHERE l.arrival = 'П') OVER (
                            PARTITION BY l.stud_id 
                            ORDER BY l.id 
                            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                        )::DECIMAL, 2)
                    )::DECIMAL, 2) AS Посещаемость,
                    l.name,
                    l.stud_id,
                    COUNT(l.name) OVER (
                            PARTITION BY l.team_id, l.stud_id 
                            ORDER BY l.id 
                            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                        ) as lesson_counter,
                    {sub_query_field}
                FROM lesson l
                {speciality_join}
                WHERE l.team_id IN ({teams_true}) and l.team_id != 749
                {speciality_cond}
            ) AS sub
            WHERE sub.name IN (
                'Организация функций30', 'Коллекции. Работа с файлами20', 'Управляющие конструкции50', 'Аттестация00'
            )
            {group_by}
            sub.name, sub.lesson_counter;
        """)
        result = res.fetchall()
        return await save_resp_and_return_it(result, href, start_time)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e
