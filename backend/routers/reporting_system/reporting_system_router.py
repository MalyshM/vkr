import os
import time

import pandas as pd
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
import io
import random
import string
from fastapi.responses import StreamingResponse
from logger import LOGGER
from models import connect_db_data

from routers.util_funcs import get_urls

reporting_system_page_router = APIRouter(tags=["Reporting system page"])


@reporting_system_page_router.post('/api/get_dataset', name='Reporting system:Reporting system',
                                   status_code=status.HTTP_200_OK,
                                   description=
                                   """
                                           Получает fields_dict: dict | None, filter_dict: dict | None, distinct: bool,
                                           рабочие параметры fields_dict снизу
                                           field_params = ['lesson_id', 'lesson_name', 'lesson_mark_for_work', 'lesson_arrival', 'lesson_test',
                                           'lesson_result_points', 'lesson_result_mark', 'lesson_stud_id', 'lesson_team_id',
                                           'lesson_teacher_id', 'lesson_date_of_add', 'rmup_id', 'rmup_name', 'rmup_link', 'rmup_date_of_add',
                                           'stud_id', 'stud_name', 'stud_email', 'stud_speciality', 'stud_date_of_add', 'teacher_id',
                                           'teacher_name', 'teacher_lect_or_pract', 'teacher_date_of_add', 'team_id',
                                           'team_name', 'team_rmup_id', 'team_date_of_add']
                                           рабочие параметры filter_dict это строка команд/учителей/направлений разреденных символом '_'
                                           filter_dict_true = {'teams':"","teachers":"Плотоненко Юрий Анатольевич_Трефилин Иван Андреевич","specialities":""}
                                           Returns:
                                               грубо говоря ссылку на скачивание csv файла
                                   """)
async def get_dataset(fields_dict: dict | None, filter_dict: dict | None, distinct: bool,
                      db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    href = "get_dataset"
    LOGGER.info(f"{href} start")
    print(fields_dict)
    # field_params = ['lesson_id', 'lesson_name', 'lesson_mark_for_work', 'lesson_arrival', 'lesson_test',
    #                 'lesson_result_points', 'lesson_result_mark', 'lesson_stud_id', 'lesson_team_id',
    #                 'lesson_teacher_id', 'lesson_date_of_add', 'rmup_id', 'rmup_name', 'rmup_link', 'rmup_date_of_add',
    #                 'stud_id', 'stud_name', 'stud_email', 'stud_speciality', 'stud_date_of_add', 'teacher_id',
    #                 'teacher_name', 'teacher_lect_or_pract', 'teacher_date_of_add', 'team_id',
    #                 'team_name', 'team_rmup_id', 'team_date_of_add']
    field_dict_true = {'lesson_id': "l.id", 'lesson_name': "l.name",
                       'lesson_mark_for_work': "l.mark_for_work", 'lesson_arrival': "l.arrival",
                       'lesson_test': "l.test", 'lesson_result_points': "l.result_points",
                       'lesson_result_mark': "l.result_mark",
                       'lesson_stud_id': "l.stud_id", 'lesson_team_id': "l.team_id",
                       'lesson_teacher_id': "l.teacher_id",
                       'lesson_date_of_add': "l.date_of_add", 'rmup_id': "r.id", 'rmup_name': "r.name",
                       'rmup_link': "r.link", 'rmup_date_of_add': "r.date_of_add", 'stud_id': "s.id",
                       'stud_name': "s.name", 'stud_email': "s.email", 'stud_speciality': "s.speciality",
                       'stud_date_of_add': "s.date_of_add", 'teacher_id': "t.id",
                       'teacher_name': "t.name",
                       'teacher_lect_or_pract': "t.lect_or_pract", 'teacher_date_of_add': "t.date_of_add",
                       'team_id': "t2.id", 'team_name': "t2.name", 'team_rmup_id': "t2.rmup_id",
                       'team_date_of_add': "t2.date_of_add"}
    # filter_dict_true = {'teams':"","teachers":"Плотоненко Юрий Анатольевич_Трефилин Иван Андреевич","specialities":""}
    # filter_dict = filter_dict_true
    if len(filter_dict) > 0:
        teams_str = ''
        teachers_str = ''
        specialities_str = ''
        if filter_dict['teams'] != "":
            teams = filter_dict['teams'].split("_")
            teams = ', '.join([f"'{team}'" for team in teams])
            teams_str = f'and t2.name IN ({teams})'
        if filter_dict['teachers'] != "":
            teachers = filter_dict['teachers'].split("_")
            teachers = ', '.join([f"'{teacher}'" for teacher in teachers])
            teachers_str = f'and t.name IN ({teachers})'
        if filter_dict['specialities'] != "":
            specialities = filter_dict['specialities'].split("_")
            specialities = ', '.join([f"'{speciality}'" for speciality in specialities])
            specialities_str = f'and s.speciality IN ({specialities})'
        filter_str = f'where 1=1 {teams_str}{teachers_str}{specialities_str}'
    else:
        filter_str = ''
    field_list_str = ''
    if fields_dict is not None:
        for key, value in fields_dict.items():
            field_list_str += field_dict_true[str(value)] + ','
        field_list_str = field_list_str[:-1]
    else:
        field_list_str = '*'
    if field_list_str == '':
        field_list_str = '*'
    if distinct:
        distinct_str = ' distinct '
    else:
        distinct_str = ''
    try:
        result_query = await db.execute(f"""
            SELECT {distinct_str}
                {field_list_str}
            from lesson l
            inner join teacher t on t.id = l.teacher_id 
            inner join team t2 on t2.id  = l.team_id 
            inner join stud s on s.id = l.stud_id
            inner join rmup r on r.id = t2.rmup_id
            {filter_str}
                        """)
        df = pd.DataFrame(result_query.fetchall())
        stream = io.StringIO()
        df.to_csv(stream, index=False)
        response = StreamingResponse(iter([stream.getvalue()]),
                                     media_type="text/csv"
                                     )
        response.headers["Content-Disposition"] = "attachment; filename=export.csv"
        print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
        LOGGER.info(f"{href} finish {(time.time() - start_time)}")
        return response
    except Exception as e:
        LOGGER.error(f"{href} finish Error {e}")
        raise e


@reporting_system_page_router.post('/api/reporting_system', name='Reporting system:Reporting system',
                                   status_code=status.HTTP_200_OK,
                                   description=
                                   """
                                           Получает hrefs_list: str, name_of_sheet_list: str, as_csv: bool
                                           hrefs_list это, к примеру, http://localhost:8090/api/cum_sum_points_for_stud_for_team?id_team=2&id_stud=1,http://localhost:8090/api/cum_sum_points_for_stud_for_team?id_team=2&id_stud=1
                                           name_of_sheet_list такая же строка с разделителем ',', которая называет страницы csv
                                           Returns:
                                               массив словарей с полями 'response', "url" либо ссылку на скачивает csv файла
                                   """)
async def reporting_system(hrefs_list: str, name_of_sheet_list: str, as_csv: bool):
    start_time = time.time()
    href = f"reporting_system-{hrefs_list}-{name_of_sheet_list}-{as_csv}"
    LOGGER.info(f"{href} start")
    try:
        hrefs_list = hrefs_list.split(',')
        name_of_sheet_list = name_of_sheet_list.split(',')
        res = await get_urls(hrefs_list, as_csv)
        if isinstance(res, dict):
            res = [res]
        if as_csv:
            random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=30))
            file_path = f"trash/{random_string}.xlsx"
            writer = pd.ExcelWriter(file_path, engine="xlsxwriter")
            for index, href_resp in enumerate(res, start=0):
                df = pd.DataFrame(href_resp)
                df.to_excel(writer, sheet_name=f"{name_of_sheet_list[index]}", index=False)
            writer.close()
            with open(file_path, "rb") as file:
                contents = file.read()
            response = StreamingResponse(iter([contents]),
                                         media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response.headers["Content-Disposition"] = "attachment; filename=export.xlsx"
            os.remove(file_path)
            LOGGER.info(f"{href} finish {(time.time() - start_time)}")
            return response
        else:
            LOGGER.info(f"{href} finish {(time.time() - start_time)}")
            return res
    except Exception as e:
        LOGGER.error(f"{href} finish Error {e}")
        raise e
