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

group_comparison_page_router = APIRouter(tags=["Group comparison page"])


@group_comparison_page_router.get('/api/attendance_static_stud_for_teams', name='Plot:plot',
                                  status_code=status.HTTP_200_OK,
                                  description=
                                  """
                                          Получает id_team1: int, id_team2: int,
                                          Returns:
                                              [{'name': row[0], 'id': row[1], 'team_name': row[2], 'arrival': row[3], 'team_id': row[4]},...]
                                          \n
                                          [
                                            {
                                              "name": "7e69e519d8b8a86e5c1346ca6fc49a63bdd52c902978b7d67748f77d74979476",
                                              "id": 859,
                                              "team_name": "ПиОА П-08.02",
                                              "arrival": 0.9545454545454546,
                                              "team_id": 2
                                            },
                                            {
                                              "name": "760abb57d6ed68ba2e3cca798a31217e8be9189fefa0bd89e215c6d700caeecd",
                                              "id": 601,
                                              "team_name": "ПиОА П-04.03",
                                              "arrival": 1,
                                              "team_id": 4
                                            },
                                            {
                                              "name": "3c2e83fffbb983d214eb3a55ad18dafd12e4b5b8c993480c0a0b7453b786c2f9",
                                              "id": 899,
                                              "team_name": "ПиОА П-08.02",
                                              "arrival": 0.9545454545454546,
                                              "team_id": 2
                                            },
                                            {
                                              "name": "cd5f76842f953535d5f545d258b8248c3f629ce1289aa7de074e47f05341152d",
                                              "id": 553,
                                              "team_name": "ПиОА П-04.03",
                                              "arrival": 1,
                                              "team_id": 4
                                            },
                                  """)
async def attendance_static_stud_for_teams(id_team1: int, id_team2: int, db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    href = f"attendance_static_stud_for_teams-{id_team1}-{id_team2}"
    LOGGER.info(f"{href} start")
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
        res = await db.execute(f"""
            SELECT DISTINCT
                (SELECT s.name FROM stud s WHERE s.id = l.stud_id) AS name,
                (SELECT s.id FROM stud s WHERE s.id = l.stud_id) AS id,
                (SELECT t.name FROM team t WHERE t.id = l.team_id) AS team_name,
                ROUND(COUNT(id) FILTER (WHERE l.arrival = 'П') OVER (PARTITION BY l.stud_id) / COUNT(id) OVER (PARTITION BY l.stud_id)::DECIMAL, 2) AS static_arrival,
                (SELECT t.id FROM team t WHERE t.id = l.team_id) AS team_id
            FROM
                lesson l
            WHERE
                l.team_id = {id_team1} OR l.team_id = {id_team2}
            order by static_arrival desc
        """)
        mas = res.fetchall()
        df_list = []
        team_a = []
        team_b = []
        dict_team = {}
        for row in mas:
            team_id = row[2]
            if team_id not in dict_team:
                dict_team[team_id] = len(dict_team)
            team = team_a if dict_team[team_id] == 0 else team_b
            team.append({'name': row[0], 'id': row[1], 'team_name': row[2], 'arrival': row[3], 'team_id': row[4]})
        for i in range(max(len(team_a), len(team_b))):
            if i < len(team_a):
                df_list.append(team_a[i])
            if i < len(team_b):
                df_list.append(team_b[i])
        return await save_resp_and_return_it(df_list, href, start_time, skip=True)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e


@group_comparison_page_router.get('/api/total_points_stud_for_teams', name='Plot:plot', status_code=status.HTTP_200_OK,
                                  description=
                                  """
                                          Получает id_team1: int, id_team2: int
                                          Returns:
                                              [{'name': row[0], 'id': row[1], 'team_name': row[2], 'total_points': row[3], 'team_id': row[4]},...]
                                          \n
                                          [
                                            {
                                              "name": "1d2e6ef2292169073155afe2f7b4b27d158f4b0f1642911ab52ac88258505e8a",
                                              "id": 185,
                                              "team_name": "ПиОА П-08.02",
                                              "total_points": 96.93,
                                              "team_id": 2
                                            },
                                            {
                                              "name": "7d2e36f95f2530714b85f21a08c5c4bf6b8c59f6fbdc50ce1b22efac5a7e521f",
                                              "id": 300,
                                              "team_name": "ПиОА П-04.03",
                                              "total_points": 95.97,
                                              "team_id": 4
                                            },
                                            {
                                              "name": "809735612a2046a206b1d11a71013781f00835befef1318d5cfb8568398686b7",
                                              "id": 709,
                                              "team_name": "ПиОА П-08.02",
                                              "total_points": 92.61,
                                              "team_id": 2
                                            },
                                            {
                                              "name": "107183af1dc1bb923b4f7163d8e0de1af69f3da43b9797eec9db66727f51f854",
                                              "id": 289,
                                              "team_name": "ПиОА П-04.03",
                                              "total_points": 94.06,
                                              "team_id": 4
                                            },
                                  """)
async def total_points_stud_for_teams(id_team1: int, id_team2: int, db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    href = f"total_points_stud_for_teams-{id_team1}-{id_team2}"
    LOGGER.info(f"{href} start")
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
        res = await db.execute(f"""
                SELECT DISTINCT
                    (SELECT s.name FROM stud s WHERE s.id = l.stud_id) AS name,
                    (SELECT s.id FROM stud s WHERE s.id = l.stud_id) AS id,
                    (SELECT t.name FROM team t WHERE t.id = l.team_id) AS team_name,
                    ROUND((SUM(l.mark_for_work) OVER (PARTITION BY stud_id) + SUM(l.test) OVER (PARTITION BY stud_id))::DECIMAL, 2) AS cum_sum,
                    (SELECT t.id FROM team t WHERE t.id = l.team_id) AS team_id
                FROM
                    lesson l
                WHERE
                    l.team_id = {id_team1} OR l.team_id = {id_team2}
                order by cum_sum desc
            """)
        mas = res.fetchall()
        df_list = []
        team_a = []
        team_b = []
        dict_team = {}
        for row in mas:
            team_id = row[2]
            if team_id not in dict_team:
                dict_team[team_id] = len(dict_team)
            team = team_a if dict_team[team_id] == 0 else team_b
            team.append({'name': row[0], 'id': row[1], 'team_name': row[2], 'total_points': row[3], 'team_id': row[4]})
        for i in range(max(len(team_a), len(team_b))):
            if i < len(team_a):
                df_list.append(team_a[i])
            if i < len(team_b):
                df_list.append(team_b[i])
        return await save_resp_and_return_it(df_list, href, start_time, skip=True)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e


@group_comparison_page_router.get('/api/attendance_static_stud_for_all_teams', name='Plot:plot',
                                  status_code=status.HTTP_200_OK,
                                  description=
                                  """
                                          Получает token: str
                                          Returns:
                                              [{'team_name': row[0], 'arrival': row[1], 'team_id': row[2], 'teacher_id': row[3], 'teacher_name': row[4]},...]
                                          \n
                                          [
                                            {
                                              "team_name": "ПиОА Л-08",
                                              "arrival": 68.51851851851852,
                                              "team_id": 1,
                                              "teacher_id": 1,
                                              "teacher_name": "Плотоненко Юрий Анатольевич"
                                            },
                                            {
                                              "team_name": "ПиОА П-08.02",
                                              "arrival": 77.87878787878788,
                                              "team_id": 2,
                                              "teacher_id": 2,
                                              "teacher_name": "Трефилин Иван Андреевич"
                                            },
                                  """)
async def attendance_static_stud_for_all_teams(token: str, db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    href = f"attendance_static_stud_for_all_teams-{token}"
    LOGGER.info(f"{href} start")
    res = await process_href(href, start_time)
    if res is not None:
        return res
    teams = await get_teams_for_user_private(token, db)
    teams_true = ', '.join([f"'{team['id']}'" for team in teams])
    try:
        res = await db.execute(f"""
            SELECT distinct
                (SELECT t.name FROM team t WHERE t.id = l.team_id) AS team_name,
                ROUND(COUNT(id) FILTER (WHERE l.arrival = 'П') OVER (PARTITION BY l.team_id) / COUNT(id) OVER (PARTITION BY l.team_id)::DECIMAL, 2) AS arrival,
                (SELECT t.id FROM team t WHERE t.id = l.team_id) AS team_id,
                (SELECT t.id FROM teacher t WHERE t.id = l.teacher_id) AS teacher_id,
                (SELECT t.name FROM teacher t WHERE t.id = l.teacher_id) AS teacher_name
            FROM
                lesson l
            where
                l.team_id in ({teams_true})
            order by arrival desc
        """)
        result = res.fetchall()
        return await save_resp_and_return_it(result, href, start_time)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e


@group_comparison_page_router.get('/api/total_points_studs_for_all_teams', name='Plot:plot',
                                  status_code=status.HTTP_200_OK,
                                  description=
                                  """
                                          Получает token: str
                                          Returns:
                                              [{'team_name': row[0], 'avg_total_points': row[1], 'team_id': row[2], 'teacher_id': row[3], 'teacher_name': row[4]},...]
                                          \n
                                          [
                                            {
                                              "team_name": "ПиОА Л-08",
                                              "avg_total_points": 0,
                                              "team_id": 1,
                                              "teacher_id": 1,
                                              "teacher_name": "Плотоненко Юрий Анатольевич"
                                            },
                                            {
                                              "team_name": "ПиОА П-08.02",
                                              "avg_total_points": 67.72099666666666,
                                              "team_id": 2,
                                              "teacher_id": 2,
                                              "teacher_name": "Трефилин Иван Андреевич"
                                            },
                                  """)
async def total_points_studs_for_all_teams(token: str, db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    teams = await get_teams_for_user_private_without_lect(token, db)
    teams_true = ', '.join([f"'{team['id']}'" for team in teams])
    href = f"total_points_studs_for_all_teams-{token}"
    LOGGER.info(f"{href} start")
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
        res = await db.execute(f"""
            SELECT
                (SELECT t.name FROM team t WHERE t.id = l.team_id) AS team_name,
                ROUND(((SUM(l.mark_for_work) + SUM(l.test))/COUNT(DISTINCT stud_id))::DECIMAL, 2) AS avg_total_points,
                (SELECT t.id FROM team t WHERE t.id = l.team_id) AS team_id,
                (SELECT t.id FROM teacher t WHERE t.id = l.teacher_id) AS teacher_id,
                (SELECT t.name FROM teacher t WHERE t.id = l.teacher_id) AS teacher_name
            FROM
                lesson l
            WHERE
                l.team_id IN ({teams_true})
            GROUP BY
                team_id, teacher_id, teacher_name, team_name
            ORDER BY
                avg_total_points DESC;
            """)
        result = res.fetchall()
        return await save_resp_and_return_it(result, href, start_time)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e


@group_comparison_page_router.get('/api/team_kr_total_points_attendance_dynamic', name='Plot:plot',
                                  status_code=status.HTTP_200_OK,
                                  description=
                                  """
                                          Получает token: str, group_by_teacher, teacher_list (пример "Павлова Елена Александровна,Павлова Елена Александровна")

                                          [
                                            {
                                              "team_name": "ПиОА П-01.01 Спорт Прогрм", название команды
                                              "team_id": 35, айди команды
                                              "teacher_id": 4, айди преподавателя
                                              "teacher_name": "Павлова Елена Александровна", название преподавателя
                                              "Успеваемость_средняя": 31.77, средняя успеваемость команды на определенном майлстоуне
                                              "Посещаемость_средняя": 0.94 средняя посещаемость команды на определенном майлстоуне
                                            },
                                            {
                                              "team_name": "ПиОА П-01.01 Спорт Прогрм",
                                              "team_id": 35,
                                              "teacher_id": 4,
                                              "teacher_name": "Павлова Елена Александровна",
                                              "Успеваемость_средняя": 53.28,
                                              "Посещаемость_средняя": 0.94
                                            },
                                            {
                                              "team_name": "ПиОА П-01.01 Спорт Прогрм",
                                              "team_id": 35,
                                              "teacher_id": 4,
                                              "teacher_name": "Павлова Елена Александровна",
                                              "Успеваемость_средняя": 84.11,
                                              "Посещаемость_средняя": 0.93
                                            },
                                            {
                                              "team_name": "ПиОА П-01.01 Спорт Прогрм",
                                              "team_id": 35,
                                              "teacher_id": 4,
                                              "teacher_name": "Павлова Елена Александровна",
                                              "Успеваемость_средняя": 86.43,
                                              "Посещаемость_средняя": 0.89
                                            },
                                  """)
async def team_kr_total_points_attendance_dynamic(token: str, group_by_teacher: bool,
                                                  teacher_list: Optional[str] = None,
                                                  db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    teams = await get_teams_for_user_private_without_lect(token, db)
    if teacher_list is not None:
        teacher_arr = teacher_list.split(',')
        teams = await get_teams_for_param_private_without_lect(teacher_arr=teacher_arr, db=db)
    teams_true = ', '.join([f"'{team['id']}'" for team in teams])
    if group_by_teacher:
        fields = """"""
        partition_by = "sub.name, sub.teacher_id"
    else:
        fields = """sub.team_name,
                    sub.team_id,"""
        partition_by = "sub.name, sub.teacher_id, sub.team_id"
    href = f"team_kr_total_points_attendance_dynamic-{token}-{group_by_teacher}-{teacher_list}"
    LOGGER.info(f"{href} start")
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
        res = await db.execute(f"""
            SELECT DISTINCT
                {fields}
                sub.teacher_id,
                sub.teacher_name,
                ROUND(AVG(sub.Успеваемость) OVER (PARTITION BY {partition_by})::DECIMAL, 2) AS Успеваемость_средняя,
                ROUND(AVG(sub.dynamical_arrival) OVER (PARTITION BY {partition_by}) * 100::DECIMAL, 2) AS Посещаемость_средняя
            FROM
                (
                    SELECT
                        (
                            SELECT t.name FROM team t WHERE t.id = l.team_id
                        ) AS team_name,
                        ROUND(
                            (
                                SUM(l.mark_for_work) OVER (PARTITION BY stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) +
                                SUM(l.test) OVER (PARTITION BY stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
                            )::DECIMAL,
                            2
                        ) AS Успеваемость,
                        ROUND(
                            COUNT(id) FILTER (WHERE l.arrival = 'П') OVER (PARTITION BY l.stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) / 
                            COUNT(id) OVER (PARTITION BY l.stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)::DECIMAL,
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
                    WHERE
                        l.team_id IN ({teams_true})
                ) AS sub
            WHERE
                sub.name IN ('Организация функций30', 'Коллекции. Работа с файлами20', 'Управляющие конструкции50', 'Аттестация00');
            """)
        result = res.fetchall()
        result_dicts = [row._asdict() for row in result]
        result_true = []
        kostil_counter = 0
        if group_by_teacher:
            for row_dict in result_dicts:
                found = False
                if kostil_counter == 3:
                    kostil_counter = 0
                for index, result_row in enumerate(result_true):
                    if row_dict['teacher_id'] == result_row['teacher_id']:
                        result_true[index]['Успеваемость_средняя' + str(kostil_counter)] = float(
                            row_dict['Успеваемость_средняя'])
                        result_true[index]['Посещаемость_средняя' + str(kostil_counter)] = float(
                            row_dict['Посещаемость_средняя'])
                        kostil_counter += 1
                        found = True
                        break
                if not found:
                    result_true.append({
                        'teacher_id': row_dict['teacher_id'],
                        'teacher_name': row_dict['teacher_name'],
                        'Успеваемость_средняя': float(row_dict['Успеваемость_средняя']),
                        'Посещаемость_средняя': float(row_dict['Посещаемость_средняя'])
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
                        result_true[index]['Посещаемость_средняя' + str(kostil_counter)] = float(
                            row_dict['Посещаемость_средняя'])
                        kostil_counter += 1
                        found = True
                        break
                if not found:
                    result_true.append({
                        'team_name': row_dict['team_name'], 'team_id': row_dict['team_id'],
                        'teacher_id': row_dict['teacher_id'],
                        'teacher_name': row_dict['teacher_name'],
                        'Успеваемость_средняя': float(row_dict['Успеваемость_средняя']),
                        'Посещаемость_средняя': float(row_dict['Посещаемость_средняя'])
                    })
        return await save_resp_and_return_it(result_true, href, start_time, skip=True)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e


@group_comparison_page_router.get('/api/team_kr_total_points_dynamic', name='Plot:plot', status_code=status.HTTP_200_OK,
                                  description=
                                  """
                                          Получает token: str, group_by_teacher, teacher_list (пример "Павлова Елена Александровна,Павлова Елена Александровна")

                                          [
                                            {
                                              "team_name": "ПиОА П-01.01 Спорт Прогрм", название команды
                                              "team_id": 35, айди команды
                                              "teacher_id": 4, айди преподавателя
                                              "teacher_name": "Павлова Елена Александровна", название преподавателя
                                              "Успеваемость_средняя": 31.77 средняя успеваемость команды на определенном майлстоуне
                                            },
                                            {
                                              "team_name": "ПиОА П-01.01 Спорт Прогрм",
                                              "team_id": 35,
                                              "teacher_id": 4,
                                              "teacher_name": "Павлова Елена Александровна",
                                              "Успеваемость_средняя": 53.28
                                            },
                                            {
                                              "team_name": "ПиОА П-01.01 Спорт Прогрм",
                                              "team_id": 35,
                                              "teacher_id": 4,
                                              "teacher_name": "Павлова Елена Александровна",
                                              "Успеваемость_средняя": 84.11
                                            },
                                            {
                                              "team_name": "ПиОА П-01.01 Спорт Прогрм",
                                              "team_id": 35,
                                              "teacher_id": 4,
                                              "teacher_name": "Павлова Елена Александровна",
                                              "Успеваемость_средняя": 86.43
                                            },
                                  """)
async def team_kr_total_points_dynamic(token: str, group_by_teacher: bool,
                                       teacher_list: Optional[str] = None,
                                       db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    teams = await get_teams_for_user_private_without_lect(token, db)
    if teacher_list is not None:
        teacher_arr = teacher_list.split(',')
        teams = await get_teams_for_param_private_without_lect(teacher_arr=teacher_arr, db=db)
    teams_true = ', '.join([f"'{team['id']}'" for team in teams])
    if group_by_teacher:
        fields = """"""
        partition_by = "sub.name, sub.teacher_id"
    else:
        fields = """sub.team_name,
                    sub.team_id,"""
        partition_by = "sub.name, sub.teacher_id, sub.team_id"
    href = f"team_kr_total_points_dynamic-{token}-{group_by_teacher}--{teacher_list}"
    LOGGER.info(f"{href} start")
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
        res = await db.execute(f"""
            SELECT DISTINCT
                {fields}
                sub.teacher_id,
                sub.teacher_name,
                ROUND(AVG(sub.Успеваемость) OVER (PARTITION BY {partition_by})::DECIMAL, 2) AS Успеваемость_средняя
            FROM
                (
                    SELECT
                        (
                            SELECT t.name FROM team t WHERE t.id = l.team_id
                        ) AS team_name,
                        ROUND(
                            (
                                SUM(l.mark_for_work) OVER (PARTITION BY stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) +
                                SUM(l.test) OVER (PARTITION BY stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
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
                    WHERE
                        l.team_id IN ({teams_true})
                ) AS sub
            WHERE
                sub.name IN ('Организация функций30', 'Коллекции. Работа с файлами20', 'Управляющие конструкции50', 'Аттестация00');
            """)
        result = res.fetchall()
        result_dicts = [row._asdict() for row in result]
        result_true = []
        kostil_counter = 0
        if group_by_teacher:
            for row_dict in result_dicts:
                found = False
                if kostil_counter == 3:
                    kostil_counter = 0
                for index, result_row in enumerate(result_true):
                    if row_dict['teacher_id'] == result_row['teacher_id']:
                        result_true[index]['Успеваемость_средняя' + str(kostil_counter)] = float(
                            row_dict['Успеваемость_средняя'])
                        kostil_counter += 1
                        found = True
                        break
                if not found:
                    result_true.append({
                        'teacher_id': row_dict['teacher_id'],
                        'teacher_name': row_dict['teacher_name'],
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
                        'team_name': row_dict['team_name'], 'team_id': row_dict['team_id'],
                        'teacher_id': row_dict['teacher_id'],
                        'teacher_name': row_dict['teacher_name'],
                        'Успеваемость_средняя': float(row_dict['Успеваемость_средняя'])
                    })
        return await save_resp_and_return_it(result_true, href, start_time, skip=True)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e


@group_comparison_page_router.get('/api/team_kr_attendance_dynamic', name='Plot:plot', status_code=status.HTTP_200_OK,
                                  tags=["Group comparison page"], description=
                                  """
                                          Получает token: str, group_by_teacher, teacher_list (пример "Павлова Елена Александровна,Павлова Елена Александровна")

                                          [
                                            {
                                              "team_name": "ПиОА П-01.01 Спорт Прогрм", название команды
                                              "team_id": 35, айди команды
                                              "teacher_id": 4, айди преподавателя
                                              "teacher_name": "Павлова Елена Александровна", название преподавателя
                                              "Посещаемость_средняя": 0.94 средняя посещаемость команды на определенном майлстоуне
                                            },
                                            {
                                              "team_name": "ПиОА П-01.01 Спорт Прогрм",
                                              "team_id": 35,
                                              "teacher_id": 4,
                                              "teacher_name": "Павлова Елена Александровна",
                                              "Посещаемость_средняя": 0.94
                                            },
                                            {
                                              "team_name": "ПиОА П-01.01 Спорт Прогрм",
                                              "team_id": 35,
                                              "teacher_id": 4,
                                              "teacher_name": "Павлова Елена Александровна",
                                              "Посещаемость_средняя": 0.93
                                            },
                                            {
                                              "team_name": "ПиОА П-01.01 Спорт Прогрм",
                                              "team_id": 35,
                                              "teacher_id": 4,
                                              "teacher_name": "Павлова Елена Александровна",
                                              "Посещаемость_средняя": 0.89
                                            },
                                  """)
async def team_kr_attendance_dynamic(token: str, group_by_teacher: bool,
                                     teacher_list: Optional[str] = None,
                                     db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    teams = await get_teams_for_user_private_without_lect(token, db)
    if teacher_list is not None:
        teacher_arr = teacher_list.split(',')
        teams = await get_teams_for_param_private_without_lect(teacher_arr=teacher_arr, db=db)
    teams_true = ', '.join([f"'{team['id']}'" for team in teams])
    if group_by_teacher:
        fields = """"""
        partition_by = "sub.name, sub.teacher_id"
    else:
        fields = """sub.team_name,
                    sub.team_id,"""
        partition_by = "sub.name, sub.teacher_id, sub.team_id"
    href = f"team_kr_attendance_dynamic-{token}-{group_by_teacher}--{teacher_list}"
    LOGGER.info(f"{href} start")
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
        res = await db.execute(f"""
            SELECT DISTINCT
                {fields}
                sub.teacher_id,
                sub.teacher_name,
                ROUND(AVG(sub.dynamical_arrival) OVER (PARTITION BY {partition_by}) * 100::DECIMAL, 2) AS Посещаемость_средняя
            FROM
                (
                    SELECT
                        (
                            SELECT t.name FROM team t WHERE t.id = l.team_id
                        ) AS team_name,
                        ROUND(
                            COUNT(id) FILTER (WHERE l.arrival = 'П') OVER (PARTITION BY l.stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) / 
                            COUNT(id) OVER (PARTITION BY l.stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)::DECIMAL,
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
                    WHERE
                        l.team_id IN ({teams_true})
                ) AS sub
            WHERE
                sub.name IN ('Организация функций30', 'Коллекции. Работа с файлами20', 'Управляющие конструкции50', 'Аттестация00');
            """)
        result = res.fetchall()
        result_dicts = [row._asdict() for row in result]
        result_true = []
        kostil_counter = 0
        if group_by_teacher:
            for row_dict in result_dicts:
                found = False
                if kostil_counter == 3:
                    kostil_counter = 0
                for index, result_row in enumerate(result_true):
                    if row_dict['teacher_id'] == result_row['teacher_id']:
                        result_true[index]['Посещаемость_средняя' + str(kostil_counter)] = float(
                            row_dict['Посещаемость_средняя'])
                        kostil_counter += 1
                        found = True
                        break
                if not found:
                    result_true.append({
                        'teacher_id': row_dict['teacher_id'],
                        'teacher_name': row_dict['teacher_name'],
                        'Посещаемость_средняя': float(row_dict['Посещаемость_средняя'])
                    })
        else:
            for row_dict in result_dicts:
                found = False
                if kostil_counter == 3:
                    kostil_counter = 0
                for index, result_row in enumerate(result_true):
                    if row_dict['team_id'] == result_row['team_id']:
                        result_true[index]['Посещаемость_средняя' + str(kostil_counter)] = float(
                            row_dict['Посещаемость_средняя'])
                        kostil_counter += 1
                        found = True
                        break
                if not found:
                    result_true.append({
                        'team_name': row_dict['team_name'], 'team_id': row_dict['team_id'],
                        'teacher_id': row_dict['teacher_id'],
                        'teacher_name': row_dict['teacher_name'],
                        'Посещаемость_средняя': float(row_dict['Посещаемость_средняя'])
                    })
        return await save_resp_and_return_it(result_true, href, start_time, skip=True)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e
