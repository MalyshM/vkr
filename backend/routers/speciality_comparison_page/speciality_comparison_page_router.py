import time

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing import Optional
from logger import LOGGER
from models import connect_db_data
from redis import process_href, save_resp_and_return_it
from routers.util_funcs import get_teams_for_user_private, get_teams_for_user_private_without_lect, \
    get_teams_for_param_private_without_lect

from routers.util.util_router import get_all_specialities_by_teacher_arr, get_all_specialities

speciality_comparison_page_router = APIRouter(tags=["Speciality comparison page"])


@speciality_comparison_page_router.get('/api/attendance_static_for_specialities', name='Plot:plot',
                                       status_code=status.HTTP_200_OK,
                                       description=
                                       """
                                               Получает token: str, speciality1: str, speciality2: str, lect: bool,
                                               Returns:
                                                   [{'arrival': row[0], 'speciality': row[1], 'id': row[2]},...]
                                               \n
                                               [
                                                 {
                                                   "arrival": 100,
                                                   "speciality": "10.05.03 Информационная безопасность автоматизированных систем",
                                                   "id": 2
                                                 },
                                                 {
                                                   "arrival": 96.42857142857143,
                                                   "speciality": "01.03.03 Механика и математическое моделирование",
                                                   "id": 67
                                                 },
                                       """)
async def attendance_static_for_specialities(token: str, speciality1: str, speciality2: str, lect: bool,
                                             db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    if lect:
        teams = await get_teams_for_user_private(token, db)
    else:
        teams = await get_teams_for_user_private_without_lect(token, db)
    teams_true = ', '.join([f"'{team['id']}'" for team in teams])
    href = f"attendance_static_for_specialities-{token}-{speciality1}--{speciality2}--{lect}"
    LOGGER.info(f"{href} start")
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
        res = await db.execute(f"""
            SELECT DISTINCT
                ROUND(COUNT(l.id) FILTER (WHERE l.arrival = 'П') OVER (PARTITION BY l.stud_id) / COUNT(l.id) OVER (PARTITION BY l.stud_id)::DECIMAL, 2) AS arrival,
                s.speciality AS speciality,
                s.id AS id
            FROM
                lesson l
            inner join stud s on s.id = l.stud_id
            WHERE
                l.team_id IN ({teams_true})
                and (s.speciality = '{speciality1}' or s.speciality = '{speciality2}')
            order by arrival desc
            """)
        mas = res.fetchall()
        df_list = []
        team_a = []
        team_b = []
        dict_team = {}
        for row in mas:
            team_id = row[1]
            if team_id not in dict_team:
                dict_team[team_id] = len(dict_team)
            team = team_a if dict_team[team_id] == 0 else team_b
            team.append({'arrival': row[0], 'speciality': row[1], 'id': row[2]})
        for i in range(max(len(team_a), len(team_b))):
            if i < len(team_a):
                df_list.append(team_a[i])
            if i < len(team_b):
                df_list.append(team_b[i])
        return await save_resp_and_return_it(df_list, href, start_time, skip=True)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e


@speciality_comparison_page_router.get('/api/total_points_for_specialities', name='Plot:plot',
                                       status_code=status.HTTP_200_OK,
                                       description=
                                       """
                                               Получает token: str, speciality1: str, speciality2: str, lect: bool,
                                               Returns:
                                                   [{'total_points': row[0], 'speciality': row[1], 'id': row[2]},...]
                                               \n
                                               [
                                                 {
                                                   "total_points": 93.21,
                                                   "speciality": "10.05.03 Информационная безопасность автоматизированных систем",
                                                   "id": 727
                                                 },
                                                 {
                                                   "total_points": 91.3,
                                                   "speciality": "01.03.03 Механика и математическое моделирование",
                                                   "id": 387
                                                 },
                                                 {
                                                   "total_points": 91.8,
                                                   "speciality": "10.05.03 Информационная безопасность автоматизированных систем",
                                                   "id": 192
                                                 },
                                       """)
async def total_points_for_specialities(token: str, speciality1: str, speciality2: str, lect: bool,
                                        db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    if lect:
        teams = await get_teams_for_user_private(token, db)
    else:
        teams = await get_teams_for_user_private_without_lect(token, db)
    teams_true = ', '.join([f"'{team['id']}'" for team in teams])
    href = f"total_points_for_specialities-{token}-{speciality1}--{speciality2}--{lect}"
    LOGGER.info(f"{href} start")
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
        res = await db.execute(f"""
                SELECT DISTINCT
                    ROUND((SUM(l.mark_for_work) OVER (PARTITION BY stud_id) + SUM(l.test) OVER (PARTITION BY stud_id))::DECIMAL, 2) AS total_points,
                    s.speciality AS speciality,
                    s.id AS id
                FROM
                    lesson l
                inner join stud s on s.id = l.stud_id
                WHERE
                    l.team_id IN ({teams_true})
                    and (s.speciality = '{speciality1}' or s.speciality = '{speciality2}')
                order by total_points desc
                """)
        mas = res.fetchall()
        df_list = []
        team_a = []
        team_b = []
        dict_team = {}
        for row in mas:
            team_id = row[1]
            if team_id not in dict_team:
                dict_team[team_id] = len(dict_team)
            team = team_a if dict_team[team_id] == 0 else team_b
            team.append({'total_points': row[0] if row[0] > 0 else 0, 'speciality': row[1], 'id': row[2]})
        for i in range(max(len(team_a), len(team_b))):
            if i < len(team_a):
                df_list.append(team_a[i])
            if i < len(team_b):
                df_list.append(team_b[i])
        return await save_resp_and_return_it(df_list, href, start_time, skip=True)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e


@speciality_comparison_page_router.get('/api/attendance_static_stud_for_all_specialities', name='Plot:plot',
                                       status_code=status.HTTP_200_OK,
                                       description=
                                       """
                                               Получает token: str, lect: bool,
                                               Returns:
                                                   [{'arrival': row[0], 'Stud_speciality': row[1], 'studs_in_speciality': row[2]},...]
                                               \n
                                               [
                                                 {
                                                   "arrival": 67.85714285714286,
                                                   "Stud_speciality": "01.03.01 Математика",
                                                   "studs_in_speciality": 22
                                                 },
                                                 {
                                                   "arrival": 75.31055900621118,
                                                   "Stud_speciality": "01.03.03 Механика и математическое моделирование",
                                                   "studs_in_speciality": 23
                                                 },
                                       """)
async def attendance_static_stud_for_all_specialities(token: str, lect: bool,
                                                      db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    if lect:
        teams = await get_teams_for_user_private(token, db)
    else:
        teams = await get_teams_for_user_private_without_lect(token, db)
    teams_true = ', '.join([f"'{team['id']}'" for team in teams])
    href = f"attendance_static_stud_for_all_specialities-{token}-{lect}"
    LOGGER.info(f"{href} start")
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
        res = await db.execute(f"""
            SELECT
                ROUND(COUNT(l.id) FILTER (WHERE l.arrival = 'П') / COUNT(l.id)::DECIMAL, 2) AS arrival,
                s.speciality AS Stud_speciality,
                count(distinct s.id) AS studs_in_speciality
            FROM
                lesson l
            inner join stud s on s.id = l.stud_id
            WHERE
                l.team_id IN ({teams_true})
            group by s.speciality 
            order by arrival desc
                    """)
        result = res.fetchall()
        return await save_resp_and_return_it(result, href, start_time)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e


@speciality_comparison_page_router.get('/api/total_points_studs_for_all_specialities', name='Plot:plot',
                                       status_code=status.HTTP_200_OK,
                                       description=
                                       """
                                               Получает token: str, lect: bool,
                                               Returns:
                                                   [{'Stud_speciality': row[0], 'avg_total_points': row[2] / row[1], 'studs_in_speciality': row[1]},...]
                                               \n
                                               [
                                                 {
                                                   "Stud_speciality": "01.03.01 Математика",
                                                   "avg_total_points": 42.32272727272727,
                                                   "studs_in_speciality": 22
                                                 },
                                                 {
                                                   "Stud_speciality": "01.03.03 Механика и математическое моделирование",
                                                   "avg_total_points": 56.73652608695652,
                                                   "studs_in_speciality": 23
                                                 },
                                       """)
async def total_points_studs_for_all_specialities(token: str, lect: bool, db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    if lect:
        teams = await get_teams_for_user_private(token, db)
    else:
        teams = await get_teams_for_user_private_without_lect(token, db)
    teams_true = ', '.join([f"'{team['id']}'" for team in teams])
    href = f"total_points_studs_for_all_specialities-{token}-{lect}"
    LOGGER.info(f"{href} start")
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
        res = await db.execute(f"""
                select
                    s.speciality AS Stud_speciality,
                    ROUND(((SUM(l.mark_for_work) + SUM(l.test))/COUNT(DISTINCT stud_id))::DECIMAL, 2) AS avg_total_points,
                    count(distinct s.id) AS studs_in_speciality
                FROM
                    lesson l
                inner join stud s on s.id = l.stud_id
                WHERE
                    l.team_id IN ({teams_true})
                group by s.speciality 
                order by avg_total_points desc
        """)
        result = res.fetchall()
        return await save_resp_and_return_it(result, href, start_time)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e


@speciality_comparison_page_router.get('/api/attendance_static_total_points_studs_for_all_specialities',
                                       name='Plot:plot',
                                       status_code=status.HTTP_200_OK,
                                       description=
                                       """
                                               Получает token: str, lect: bool,
                                               Returns:
                                                   [{'Stud_speciality': row[0], 'avg_total_points': row[2] / row[1], 'studs_in_speciality': row[1]},...]
                                               \n
                                               [
                                                 {
                                                   "Stud_speciality": "01.03.01 Математика",
                                                   "avg_total_points": 42.32272727272727,
                                                   "studs_in_speciality": 22
                                                 },
                                                 {
                                                   "Stud_speciality": "01.03.03 Механика и математическое моделирование",
                                                   "avg_total_points": 56.73652608695652,
                                                   "studs_in_speciality": 23
                                                 },
                                       """)
async def attendance_static_total_points_studs_for_all_specialities(token: str, lect: bool,
                                                                    db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    if lect:
        teams = await get_teams_for_user_private(token, db)
    else:
        teams = await get_teams_for_user_private_without_lect(token, db)
    teams_true = ', '.join([f"'{team['id']}'" for team in teams])
    href = f"attendance_static_total_points_studs_for_all_specialities-{token}-{lect}"
    LOGGER.info(f"{href} start")
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
        res = await db.execute(f"""
                select
                    s.speciality AS Stud_speciality,
                    ROUND(((SUM(l.mark_for_work) + SUM(l.test))/COUNT(DISTINCT stud_id))::DECIMAL, 2) AS avg_total_points,
                    ROUND(COUNT(l.id) FILTER (WHERE l.arrival = 'П') / COUNT(l.id)::DECIMAL, 2) AS arrival,
                    count(distinct s.id) AS studs_in_speciality
                FROM
                    lesson l
                inner join stud s on s.id = l.stud_id
                WHERE
                    l.team_id IN ({teams_true})
                group by s.speciality 
                order by avg_total_points desc
        """)
        result = res.fetchall()
        return await save_resp_and_return_it(result, href, start_time)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e


@speciality_comparison_page_router.get('/api/speciality_kr_total_points_attendance_dynamic', name='Plot:plot',
                                       status_code=status.HTTP_200_OK,
                                       description=
                                       """
                                               Получает token: str, group_by_speciality, teacher_list (пример "Павлова Елена Александровна,Павлова Елена Александровна")

                                               [
                                                 {
                                                   "stud_speciality": "02.03.03 Математическое обеспечение и администрирование информационных систем", направление
                                                   "teacher_name": "Плотоненко Юрий Анатольевич", ФИО преподавателя
                                                   "teacher_id": 1, айди преподавателя
                                                   "Успеваемость_средняя": 18.83,  средняя успеваемость команды на определенном майлстоуне
                                                   "Посещаемость_средняя": 0.52 средняя посещаемость команды на определенном майлстоуне
                                                 },
                                                 {
                                                   "stud_speciality": "02.03.03 Математическое обеспечение и администрирование информационных систем",
                                                   "teacher_name": "Плотоненко Юрий Анатольевич",
                                                   "teacher_id": 1,
                                                   "Успеваемость_средняя": 35.5,
                                                   "Посещаемость_средняя": 0.51
                                                 },
                                                 {
                                                   "stud_speciality": "02.03.03 Математическое обеспечение и администрирование информационных систем",
                                                   "teacher_name": "Плотоненко Юрий Анатольевич",
                                                   "teacher_id": 1,
                                                   "Успеваемость_средняя": 50.5,
                                                   "Посещаемость_средняя": 0.53
                                                 },
                                                 {
                                                   "stud_speciality": "02.03.03 Математическое обеспечение и администрирование информационных систем",
                                                   "teacher_name": "Плотоненко Юрий Анатольевич",
                                                   "teacher_id": 1,
                                                   "Успеваемость_средняя": 53.33,
                                                   "Посещаемость_средняя": 0.52
                                                 },
                                       """)
async def speciality_kr_total_points_attendance_dynamic(token: str, group_by_speciality: bool,
                                                        teacher_list: Optional[str] = None,
                                                        speciality_list: Optional[str] = None,
                                                        db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    if teacher_list is not None:
        teacher_arr = teacher_list.split(',')
        teams = await get_teams_for_param_private_without_lect(teacher_arr=teacher_arr, db=db)
    else:
        teams = await get_teams_for_user_private_without_lect(token, db)
    teams_true = ', '.join([f"'{team['id']}'" for team in teams])
    if speciality_list is not None:
        speciality_list = speciality_list.split(',')
        speciality_list = ', '.join([f"'{speciality}'" for speciality in speciality_list])
        speciality_cond = f"AND s.speciality IN ({speciality_list})"
    else:
        speciality_cond = ""
    if group_by_speciality:
        fields = """"""
        partition_by = "sub.Stud_speciality, sub.name"
    else:
        fields = """sub.teacher_name,
                    sub.teacher_id,"""
        partition_by = "sub.Stud_speciality, sub.name, sub.teacher_id"
    href = f"speciality_kr_total_points_attendance_dynamic-{token}--{group_by_speciality}--{teacher_list}-{speciality_list}"
    LOGGER.info(f"{href} start")
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
        res = await db.execute(f"""
            SELECT DISTINCT
                sub.Stud_speciality,
                {fields}
                ROUND(AVG(sub.Успеваемость) OVER (PARTITION BY {partition_by})::DECIMAL, 2) AS Успеваемость_средняя,
                ROUND(AVG(sub.dynamical_arrival) OVER (PARTITION BY {partition_by}) * 100::DECIMAL, 2) AS Посещаемость_средняя
            FROM
                (
                    SELECT
                        s.speciality AS Stud_speciality,
                        ROUND(
                            (
                                SUM(l.mark_for_work) OVER (PARTITION BY l.stud_id, s.speciality ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) +
                                SUM(l.test) OVER (PARTITION BY l.stud_id, s.speciality ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
                            )::DECIMAL,
                            2
                        ) AS Успеваемость,
                        ROUND(
                            COUNT(l.id) FILTER (WHERE l.arrival = 'П') OVER (PARTITION BY l.stud_id, s.speciality ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) / 
                            COUNT(l.id) OVER (PARTITION BY l.stud_id, s.speciality ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)::DECIMAL,
                            2
                        ) AS dynamical_arrival,
                        (
                            SELECT t.id FROM team t WHERE t.id = l.team_id
                        ) AS team_id,
                        (
                            SELECT t.id FROM teacher t WHERE t.id = l.teacher_id
                        ) AS teacher_id,
                        (
                            SELECT t.name FROM teacher t WHERE t.id = l.teacher_id
                        ) AS teacher_name,
                        l.name
                    FROM
                        lesson l
                    INNER JOIN stud s ON s.id = l.stud_id
                    WHERE
                        l.team_id IN ({teams_true})
                        {speciality_cond}
                ) AS sub
            WHERE 
                sub.name IN ('Организация функций30', 'Коллекции. Работа с файлами20', 'Управляющие конструкции50', 'Аттестация00');
            """)
        result = res.fetchall()
        result_dicts = [row._asdict() for row in result]
        result_true = []
        kostil_counter = 0
        if group_by_speciality:
            for row_dict in result_dicts:
                found = False
                if kostil_counter == 3:
                    kostil_counter = 0
                for index, result_row in enumerate(result_true):
                    if row_dict['stud_speciality'] == result_row['stud_speciality']:
                        result_true[index]['Успеваемость_средняя' + str(kostil_counter)] = float(
                            row_dict['Успеваемость_средняя'])
                        result_true[index]['Посещаемость_средняя' + str(kostil_counter)] = float(
                            row_dict['Посещаемость_средняя'])
                        kostil_counter += 1
                        found = True
                        break
                if not found:
                    result_true.append({
                        'stud_speciality': row_dict['stud_speciality'],
                        'Успеваемость_средняя': float(row_dict['Успеваемость_средняя']),
                        'Посещаемость_средняя': float(row_dict['Посещаемость_средняя'])
                    })
        else:
            for row_dict in result_dicts:
                found = False
                if kostil_counter == 3:
                    kostil_counter = 0
                for index, result_row in enumerate(result_true):
                    if row_dict['teacher_id'] == result_row['teacher_id'] and row_dict['stud_speciality'] == result_row[
                        'stud_speciality']:
                        result_true[index]['Успеваемость_средняя' + str(kostil_counter)] = float(
                            row_dict['Успеваемость_средняя'])
                        result_true[index]['Посещаемость_средняя' + str(kostil_counter)] = float(
                            row_dict['Посещаемость_средняя'])
                        kostil_counter += 1
                        found = True
                        break
                if not found:
                    result_true.append({
                        'stud_speciality': row_dict['stud_speciality'],
                        'teacher_name': row_dict['teacher_name'], 'teacher_id': row_dict['teacher_id'],
                        'Успеваемость_средняя': float(row_dict['Успеваемость_средняя']),
                        'Посещаемость_средняя': float(row_dict['Посещаемость_средняя'])
                    })
        return await save_resp_and_return_it(result_true, href, start_time, skip=True)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e


@speciality_comparison_page_router.get('/api/speciality_kr_attendance_dynamic', name='Plot:plot',
                                       status_code=status.HTTP_200_OK,
                                       description=
                                       """
                                               Получает token: str, group_by_speciality, teacher_list (пример "Павлова Елена Александровна,Павлова Елена Александровна")

                                               [
                                                 {
                                                   "stud_speciality": "02.03.03 Математическое обеспечение и администрирование информационных систем", направление
                                                   "teacher_name": "Плотоненко Юрий Анатольевич", ФИО преподавателя
                                                   "teacher_id": 1, айди преподавателя
                                                   "Посещаемость_средняя": 0.52 средняя посещаемость команды на определенном майлстоуне
                                                 },
                                                 {
                                                   "stud_speciality": "02.03.03 Математическое обеспечение и администрирование информационных систем",
                                                   "teacher_name": "Плотоненко Юрий Анатольевич",
                                                   "teacher_id": 1,
                                                   "Посещаемость_средняя": 0.51
                                                 },
                                                 {
                                                   "stud_speciality": "02.03.03 Математическое обеспечение и администрирование информационных систем",
                                                   "teacher_name": "Плотоненко Юрий Анатольевич",
                                                   "teacher_id": 1,
                                                   "Посещаемость_средняя": 0.53
                                                 },
                                                 {
                                                   "stud_speciality": "02.03.03 Математическое обеспечение и администрирование информационных систем",
                                                   "teacher_name": "Плотоненко Юрий Анатольевич",
                                                   "teacher_id": 1,
                                                   "Посещаемость_средняя": 0.52
                                                 },
                                       """)
async def speciality_kr_attendance_dynamic(token: str, group_by_speciality: bool,
                                           teacher_list: Optional[str] = None,
                                           speciality_list: Optional[str] = None,
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
    if group_by_speciality:
        fields = """"""
        partition_by = "sub.Stud_speciality, sub.name"
    else:
        fields = """sub.teacher_name,
                    sub.teacher_id,"""
        partition_by = "sub.Stud_speciality, sub.name, sub.teacher_id"
    href = f"speciality_kr_attendance_dynamic-{token}--{group_by_speciality}--{teacher_list}-{speciality_list}"
    LOGGER.info(f"{href} start")
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
        res = await db.execute(f"""
            SELECT DISTINCT
                sub.Stud_speciality,
                {fields}
                ROUND(AVG(sub.dynamical_arrival) OVER (PARTITION BY {partition_by}) * 100::DECIMAL, 2) AS Посещаемость_средняя
            FROM
                (
                    SELECT
                        s.speciality AS Stud_speciality,
                        ROUND(
                            COUNT(l.id) FILTER (WHERE l.arrival = 'П') OVER (PARTITION BY l.stud_id, s.speciality ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) / 
                            COUNT(l.id) OVER (PARTITION BY l.stud_id, s.speciality ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)::DECIMAL,
                            2
                        ) AS dynamical_arrival,
                        (
                            SELECT t.id FROM team t WHERE t.id = l.team_id
                        ) AS team_id,
                        (
                            SELECT t.id FROM teacher t WHERE t.id = l.teacher_id
                        ) AS teacher_id,
                        (
                            SELECT t.name FROM teacher t WHERE t.id = l.teacher_id
                        ) AS teacher_name,
                        l.name
                    FROM
                        lesson l
                    INNER JOIN stud s ON s.id = l.stud_id
                    WHERE
                        l.team_id IN ({teams_true})
                        {speciality_cond}
                ) AS sub
            WHERE 
                sub.name IN ('Организация функций30', 'Коллекции. Работа с файлами20', 'Управляющие конструкции50', 'Аттестация00');
            """)
        result = res.fetchall()
        result_dicts = [row._asdict() for row in result]
        result_true = []
        kostil_counter = 0
        if group_by_speciality:
            for row_dict in result_dicts:
                found = False
                if kostil_counter == 3:
                    kostil_counter = 0
                for index, result_row in enumerate(result_true):
                    if row_dict['stud_speciality'] == result_row['stud_speciality']:
                        result_true[index]['Посещаемость_средняя' + str(kostil_counter)] = float(
                            row_dict['Посещаемость_средняя'])
                        kostil_counter += 1
                        found = True
                        break
                if not found:
                    result_true.append({
                        'stud_speciality': row_dict['stud_speciality'],
                        'Посещаемость_средняя': float(row_dict['Посещаемость_средняя'])
                    })
        else:
            for row_dict in result_dicts:
                found = False
                if kostil_counter == 3:
                    kostil_counter = 0
                for index, result_row in enumerate(result_true):
                    if row_dict['teacher_id'] == result_row['teacher_id'] and row_dict['stud_speciality'] == result_row[
                        'stud_speciality']:
                        result_true[index]['Посещаемость_средняя' + str(kostil_counter)] = float(
                            row_dict['Посещаемость_средняя'])
                        kostil_counter += 1
                        found = True
                        break
                if not found:
                    result_true.append({
                        'stud_speciality': row_dict['stud_speciality'],
                        'teacher_name': row_dict['teacher_name'], 'teacher_id': row_dict['teacher_id'],
                        'Посещаемость_средняя': float(row_dict['Посещаемость_средняя'])
                    })
        return await save_resp_and_return_it(result_true, href, start_time, skip=True)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e


@speciality_comparison_page_router.get('/api/speciality_kr_total_points_dynamic', name='Plot:plot',
                                       status_code=status.HTTP_200_OK,
                                       description=
                                       """
                                               Получает token: str, group_by_speciality, teacher_list (пример "Павлова Елена Александровна,Павлова Елена Александровна")

                                               [
                                                 {
                                                   "stud_speciality": "02.03.03 Математическое обеспечение и администрирование информационных систем", направление
                                                   "teacher_name": "Плотоненко Юрий Анатольевич", ФИО преподавателя
                                                   "teacher_id": 1, айди преподавателя
                                                   "Успеваемость_средняя": 18.83  средняя успеваемость команды на определенном майлстоуне
                                                 },
                                                 {
                                                   "stud_speciality": "02.03.03 Математическое обеспечение и администрирование информационных систем",
                                                   "teacher_name": "Плотоненко Юрий Анатольевич",
                                                   "teacher_id": 1,
                                                   "Успеваемость_средняя": 35.5
                                                 },
                                                 {
                                                   "stud_speciality": "02.03.03 Математическое обеспечение и администрирование информационных систем",
                                                   "teacher_name": "Плотоненко Юрий Анатольевич",
                                                   "teacher_id": 1,
                                                   "Успеваемость_средняя": 50.5
                                                 },
                                                 {
                                                   "stud_speciality": "02.03.03 Математическое обеспечение и администрирование информационных систем",
                                                   "teacher_name": "Плотоненко Юрий Анатольевич",
                                                   "teacher_id": 1,
                                                   "Успеваемость_средняя": 53.33
                                                 },
                                       """)
async def speciality_kr_total_points_dynamic(token: str, group_by_speciality: bool,
                                             teacher_list: Optional[str] = None,
                                             speciality_list: Optional[str] = None,
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
    if group_by_speciality:
        fields = """"""
        partition_by = "sub.Stud_speciality, sub.name"
    else:
        fields = """sub.teacher_name,
                    sub.teacher_id,"""
        partition_by = "sub.Stud_speciality, sub.name, sub.teacher_id"
    href = f"speciality_kr_total_points_dynamic-{token}--{group_by_speciality}--{teacher_list}-{speciality_list}"
    LOGGER.info(f"{href} start")
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
        res = await db.execute(f"""
            SELECT DISTINCT
                sub.Stud_speciality,
                {fields}
                ROUND(AVG(sub.Успеваемость) OVER (PARTITION BY {partition_by})::DECIMAL, 2) AS Успеваемость_средняя
            FROM
                (
                    SELECT
                        s.speciality AS Stud_speciality,
                        ROUND(
                            (
                                SUM(l.mark_for_work) OVER (PARTITION BY l.stud_id, s.speciality ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) +
                                SUM(l.test) OVER (PARTITION BY l.stud_id, s.speciality ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
                            )::DECIMAL,
                            2
                        ) AS Успеваемость,
                        (
                            SELECT t.id FROM team t WHERE t.id = l.team_id
                        ) AS team_id,
                        (
                            SELECT t.id FROM teacher t WHERE t.id = l.teacher_id
                        ) AS teacher_id,
                        (
                            SELECT t.name FROM teacher t WHERE t.id = l.teacher_id
                        ) AS teacher_name,
                        l.name
                    FROM
                        lesson l
                    INNER JOIN stud s ON s.id = l.stud_id
                    WHERE
                        l.team_id IN ({teams_true})
                        {speciality_cond}
                ) AS sub
            WHERE 
                sub.name IN ('Организация функций30', 'Коллекции. Работа с файлами20', 'Управляющие конструкции50', 'Аттестация00');
            """)
        result = res.fetchall()
        result_dicts = [row._asdict() for row in result]
        result_true = []
        kostil_counter = 0
        if group_by_speciality:
            for row_dict in result_dicts:
                found = False
                if kostil_counter == 3:
                    kostil_counter = 0
                for index, result_row in enumerate(result_true):
                    if row_dict['teacher_id'] == result_row['teacher_id'] and row_dict['stud_speciality'] == result_row[
                        'stud_speciality']:
                        result_true[index]['Успеваемость_средняя' + str(kostil_counter)] = float(
                            row_dict['Успеваемость_средняя'])
                        kostil_counter += 1
                        found = True
                        break
                if not found:
                    result_true.append({
                        'stud_speciality': row_dict['stud_speciality'],
                        'Успеваемость_средняя': float(row_dict['Успеваемость_средняя'])
                    })
        else:
            for row_dict in result_dicts:
                found = False
                if kostil_counter == 3:
                    kostil_counter = 0
                for index, result_row in enumerate(result_true):
                    if row_dict['team_id'] == result_row['team_id']:
                        result_true[index]['Успеваемость_средняя' + str(kostil_counter)] = float(
                            row_dict['Успеваемость_средняя'])
                        kostil_counter += 1
                        found = True
                        break
                if not found:
                    result_true.append({
                        'stud_speciality': row_dict['stud_speciality'],
                        'teacher_name': row_dict['teacher_name'], 'teacher_id': row_dict['teacher_id'],
                        'Успеваемость_средняя': float(row_dict['Успеваемость_средняя'])
                    })
        return await save_resp_and_return_it(result_true, href, start_time, skip=True)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e
