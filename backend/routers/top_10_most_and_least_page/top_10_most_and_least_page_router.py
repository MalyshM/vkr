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

top_10_most_and_least_page_router = APIRouter(tags=["top 10 most and least page"])


@top_10_most_and_least_page_router.get('/api/top_10_most_and_least_studs', name='Plot:plot', status_code=status.HTTP_200_OK,
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
async def top_10_most_and_least_studs(token: str, is_group_by: bool, is_by_mark: bool,
                                type_group_by: int = None,
                                teacher_list: Optional[str] = None, speciality_list: Optional[str] = None,
                                team_list: Optional[str] = None, db: AsyncSession = Depends(connect_db_data)):
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
    href = f"top_10_most_and_least_studs-{token}-{is_group_by}-{is_by_mark}-{type_group_by}-{teacher_list}-{speciality_list}-{team_list}"
    LOGGER.info(f"{href} start")
    query_field = ''
    sub_query_field = ''
    group_by = ''
    fields = """
            top_10.Успеваемость,
            top_10.Посещаемость,
            top_10.stud_id,
            """
    partition_by = 'sub.name, sub.lesson_counter'
    if is_by_mark:
        order_by_clause = """
            order by top_10.Успеваемость
        """
        wf_order = 'Успеваемость'
    else:
        order_by_clause = """
            order by top_10.Посещаемость
        """
        wf_order = 'Посещаемость'
    if is_group_by:
        fields_best = f"""
                json_agg(
                    json_build_object(
                        'Успеваемость', top_10.Успеваемость, 
                        'Посещаемость', top_10.Посещаемость, 
                        'stud_id', top_10.stud_id
                    ) {order_by_clause} DESC
                ) AS top_10_best,"""
        fields_worst = f"""
                        json_agg(
                            json_build_object(
                                'Успеваемость', top_10.Успеваемость, 
                                'Посещаемость', top_10.Посещаемость, 
                                'stud_id', top_10.stud_id
                            ) {order_by_clause} ASC
                        ) AS top_10_least,"""
        fields = None
        match type_group_by:
            case 0:
                query_field = ',top_10.team_id, top_10.team_name,top_10.teacher_id,top_10.teacher_name'
                sub_query_field = ",(SELECT t.name FROM team t WHERE t.id = l.team_id) AS team_name, l.team_id,(SELECT t.name FROM teacher t WHERE t.id = l.teacher_id) AS teacher_name, l.teacher_id"
                group_by = 'group by top_10.team_id, top_10.team_name,top_10.teacher_id,top_10.teacher_name,top_10.name, top_10.lesson_counter'
                partition_by = 'sub.team_id, sub.name, sub.lesson_counter'
                join_clause = 'sub.team_id = sub2.team_id AND'
            case 1:
                query_field = ',top_10.speciality'
                sub_query_field = ",(SELECT s.speciality FROM stud s WHERE s.id = l.stud_id)"
                group_by = 'group by top_10.speciality,top_10.name, top_10.lesson_counter'
                partition_by = 'sub.speciality, sub.name, sub.lesson_counter'
                join_clause = 'sub.speciality = sub2.speciality AND'
            case 2:
                query_field = ',top_10.teacher_id, top_10.teacher_name'
                sub_query_field = ",(SELECT t.name FROM teacher t WHERE t.id = l.teacher_id) AS teacher_name, l.teacher_id"
                group_by = 'group by top_10.teacher_id, top_10.teacher_name,top_10.name, top_10.lesson_counter'
                partition_by = 'sub.teacher_id, sub.name, sub.lesson_counter'
                join_clause = 'sub.teacher_id = sub2.teacher_id AND'
            case _:
                e = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                  detail="Неправильно выбран тип 0 - Группировка по командам, 1 - " +
                                         "Группировка по направлениям, 2 - Группировка по преподавателям")
                LOGGER.warning(f"{href} warning {e.detail}")
                raise e
        puzzle = f"""
        INNER JOIN (
                SELECT
                    {fields_best if fields is None else fields}
                    top_10.name,
                    top_10.lesson_counter
                    {query_field}
                FROM top_10
                WHERE row_num_desc <= 10
                {group_by}
            ) AS sub ON {join_clause} sub.lesson_counter = sub2.lesson_counter;
        """
    else:
        puzzle = f"""
        union all
            SELECT
                {fields}
                top_10.name,
                top_10.lesson_counter
                {query_field}
            FROM top_10
            WHERE row_num_desc <= 10
            {group_by}
        ;
        """
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
        res = await db.execute(f"""
            WITH top_10 AS (
                SELECT *,
                    ROW_NUMBER() OVER (PARTITION BY {partition_by} ORDER BY {wf_order} ASC) AS row_num_asc,
                    ROW_NUMBER() OVER (PARTITION BY {partition_by} ORDER BY {wf_order} DESC) AS row_num_desc
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
                        ) AS lesson_counter
                        {sub_query_field}
                    FROM lesson l
                    {speciality_join}
                    WHERE l.team_id IN ({teams_true})
                    {speciality_cond}
                ) AS sub
                WHERE sub.name IN (
                    'Организация функций30', 'Коллекции. Работа с файлами20', 'Управляющие конструкции50', 'Аттестация00'
                )
            )
            SELECT *
            FROM (
                SELECT
                    {fields_worst if fields is None else fields}
                    top_10.name,
                    top_10.lesson_counter
                    {query_field}
                FROM top_10
                WHERE row_num_asc <= 10
                {group_by}
            ) AS sub2
            {puzzle};
        """)
        result = res.fetchall()
        return await save_resp_and_return_it(result, href, start_time)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e

@top_10_most_and_least_page_router.get('/api/top_10_most_and_least_teams', name='Plot:plot', status_code=status.HTTP_200_OK,
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
async def top_10_most_and_least_teams(token: str, is_by_mark: bool,
                                type_group_by: int,
                                teacher_list: Optional[str] = None, speciality_list: Optional[str] = None,
                                team_list: Optional[str] = None, db: AsyncSession = Depends(connect_db_data)):
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
    href = f"top_10_most_and_least_teams-{token}-{is_by_mark}-{type_group_by}-{teacher_list}-{speciality_list}-{team_list}"
    LOGGER.info(f"{href} start")
    if is_by_mark:
        wf_order = 'Успеваемость_средняя'
    else:
        wf_order = 'Посещаемость_средняя'
    match type_group_by:
        case 0:
            query_field = """
                sub.team_id,
                (select t.name from team t where t.id = sub.team_id) as team_name,
                sub.teacher_id,
                (select t.name from teacher t where t.id = sub.teacher_id) as teacher_name,
            """
            sub_query_field = ""
            group_by = 'group by sub.name, sub.lesson_counter, sub.team_id, sub.teacher_id'
            partition_by = 'sub2.name, sub2.lesson_counter'
        case 1:
            query_field = 'sub.speciality,'
            sub_query_field = ",(SELECT s.speciality FROM stud s WHERE s.id = l.stud_id)"
            group_by = 'group by sub.speciality,sub.name, sub.lesson_counter'
            partition_by = 'sub2.speciality, sub2.name, sub2.lesson_counter'
        case 2:
            query_field = """
                sub.teacher_id,
                (select t.name from teacher t where t.id = sub.teacher_id) as teacher_name,
            """
            sub_query_field = ""
            group_by = 'group by sub.name, sub.lesson_counter, sub.teacher_id'
            partition_by = 'sub2.teacher_id, sub2.name, sub2.lesson_counter'
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
            WITH top_10 AS (
                SELECT *,
                    ROW_NUMBER() OVER (PARTITION BY {partition_by} ORDER BY {wf_order} ASC) AS row_num_asc,
                    ROW_NUMBER() OVER (PARTITION BY {partition_by} ORDER BY {wf_order} DESC) AS row_num_desc
                FROM (
                    SELECT 
                        {query_field}
                        sub.name,
                        sub.lesson_counter,
                        ROUND(PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY sub.Успеваемость)::DECIMAL, 2) AS Успеваемость_средняя,
                        ROUND(PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY sub.Посещаемость)::DECIMAL, 2) AS Посещаемость_средняя
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
                            l.team_id,
                            l.teacher_id,
                            COUNT(l.name) OVER (
                                PARTITION BY l.team_id, l.stud_id
                                ORDER BY l.id
                                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                            ) AS lesson_counter
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
                ) AS sub2
            )
            (
                SELECT * FROM top_10 WHERE row_num_asc <= 10 ORDER BY top_10.name
            )
            UNION ALL 
            (
                SELECT * FROM top_10 WHERE row_num_desc <= 10 ORDER BY top_10.name, top_10.row_num_desc ASC
            );
        """)
        result = res.fetchall()
        return await save_resp_and_return_it(result, href, start_time)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e