import datetime
import hashlib
import math
import pickle

import pandas as pd

# Specify the path to the Excel file
# todo убрать backend. до билда в докере
# todo сделать как было '/backend/backend/scripts/dataframe.csv' и ниже так же /backend/backend/scripts/ вот это добавить нужно
from models import *


def etl(file_path='/backend/scripts/трек HARD.xlsx', rmup_name='Математический анализ',
        sheets=['Информация по студентам', 'Информация по студентам_', 'Информация по студентам__',
                'Преподаватели Л, П']):
    dfs = []

    def find_teacher(row):
        if 'Л' in row['Команда']:
            teacher_type = 'лектор'
        else:
            teacher_type = 'практик'

        teacher_row = teacher_df[teacher_df['Команда'] == row['Команда']]
        for index, row in teacher_row.iterrows():
            if 'лектор' == teacher_type:
                # print(row[-1])
                return row[-1]
            else:
                # print(row[-2])
                return row[-2]

    for sheet in sheets:
        df = pd.read_excel(file_path, sheet_name=sheet)
        dfs.append(df)
    for i in range(len(sheets)):
        dfs[i] = dfs[i].loc[dfs[i]['Название РМУП'] == rmup_name]
    if dfs[-1].empty:
        print("нет прикрепленных преподавателей")
        return Exception("нет прикрепленных преподавателей")
    main_df = pd.concat(dfs[0:len(sheets) - 1], ignore_index=True)
    print(len(main_df.columns))
    main_df = main_df.dropna(axis=1, how='all')
    main_df = main_df.drop('Тип встречи', axis=1)
    print(len(main_df.columns))
    teacher_df = dfs[-1]
    print(main_df.columns)
    print(main_df.head())
    print(teacher_df.columns)
    print(teacher_df.head())
    previous = ''
    anonymized_dict = {}
    list_of_rmup = []
    list_of_rmup_link = []
    list_of_stud_fio = []
    list_of_team = []
    list_of_name_of_lesson = []
    list_of_subject_of_control = []
    list_of_mark_of_subject_of_control = []
    list_of_result_points = []
    list_of_result_mark = []
    list_of_arrival = []
    list_of_test = []
    list_of_stud_email = []
    list_of_stud_course = []
    list_of_teachers = []

    temp_list_of_subj = []
    temp_list_of_mark = []
    main_df['Преподаватель'] = main_df.apply(find_teacher, axis=1)
    # for row_index, row in main_df.iterrows():
    #     # for col_index, value in row.items():
    #     print(f"Row: {row_index}, Column: {row}")
    for index, row in main_df.iterrows():
        if len(temp_list_of_subj) > 1 and 'Посещение' in temp_list_of_subj \
                and 'Работа на учебной встрече' in temp_list_of_subj:
            # print(temp_list_of_subj)
            # print(temp_list_of_mark)
            if 'Контрольная работа' in row[5]:
                temp_list_of_subj.append(row[5])
                temp_list_of_mark.append(row[6])

                list_of_rmup.append(row[0])
                list_of_rmup_link.append(row[1])
                list_of_stud_fio.append(row[2])
                list_of_team.append(row[3])
                list_of_name_of_lesson.append(row[4])
                # print(temp_list_of_subj)
                if 'Практическое задание' in temp_list_of_subj:
                    mark = temp_list_of_mark[temp_list_of_subj.index('Работа на учебной встрече')]
                    pract = temp_list_of_mark[temp_list_of_subj.index('Практическое задание')]
                    if (mark is not pd.NA and pract is not pd.NA) and (not pd.isna(mark) and not pd.isna(pract)):
                        list_of_mark_of_subject_of_control.append(mark + pract)
                    elif mark is pd.NA or pd.isna(mark):
                        list_of_mark_of_subject_of_control.append(pract)
                    elif pract is pd.NA or pd.isna(pract):
                        list_of_mark_of_subject_of_control.append(mark)
                    else:
                        list_of_mark_of_subject_of_control.append(0)
                elif 'Письменный ответ' in temp_list_of_subj:
                    mark = temp_list_of_mark[temp_list_of_subj.index('Работа на учебной встрече')]
                    pract = temp_list_of_mark[temp_list_of_subj.index('Письменный ответ')]
                    if (mark is not pd.NA and pract is not pd.NA) and (not pd.isna(mark) and not pd.isna(pract)):
                        list_of_mark_of_subject_of_control.append(mark + pract)
                    elif mark is pd.NA or pd.isna(mark):
                        list_of_mark_of_subject_of_control.append(pract)
                    elif pract is pd.NA or pd.isna(pract):
                        list_of_mark_of_subject_of_control.append(mark)
                    else:
                        list_of_mark_of_subject_of_control.append(0)
                else:
                    list_of_mark_of_subject_of_control.append(
                        temp_list_of_mark[temp_list_of_subj.index('Работа на учебной встрече')])
                # if temp_list_of_mark[temp_list_of_subj.index('Работа на учебной встрече')] is None or math.isnan(temp_list_of_mark[temp_list_of_subj.index('Работа на учебной встрече')]):
                #     print(temp_list_of_mark[temp_list_of_subj.index('Практическое задание')])
                #     print(temp_list_of_mark[temp_list_of_subj.index('Работа на учебной встрече')])
                #     print(type(temp_list_of_mark[temp_list_of_subj.index('Работа на учебной встрече')]))
                #     print(temp_list_of_mark[temp_list_of_subj.index('Работа на учебной встрече')] is None)
                #     print(math.isnan(temp_list_of_mark[temp_list_of_subj.index('Работа на учебной встрече')]))
                #     list_of_mark_of_subject_of_control.append(
                #         temp_list_of_mark[temp_list_of_subj.index('Практическое задание')])
                # else:
                #     # print(temp_list_of_mark[temp_list_of_subj.index('Работа на учебной встрече')])


                list_of_arrival.append(temp_list_of_mark[temp_list_of_subj.index('Посещение')])
                list_of_test.append(str(temp_list_of_mark[temp_list_of_subj.index('Контрольная работа')]))

                list_of_result_points.append(row[7])
                list_of_result_mark.append(row[8])
                # list_of_stud_email.append(row[9])
                # list_of_stud_course.append(row[10])
                list_of_teachers.append(row[9])

                temp_list_of_subj.clear()
                temp_list_of_mark.clear()
                last_row = row
            else:
                list_of_rmup.append(last_row[0])
                list_of_rmup_link.append(last_row[1])
                list_of_stud_fio.append(last_row[2])
                list_of_team.append(last_row[3])
                list_of_name_of_lesson.append(last_row[4])
                if 'Практическое задание' in temp_list_of_subj:
                    mark = temp_list_of_mark[temp_list_of_subj.index('Работа на учебной встрече')]
                    pract = temp_list_of_mark[temp_list_of_subj.index('Практическое задание')]
                    if (mark is not pd.NA and pract is not pd.NA) and (not pd.isna(mark) and not pd.isna(pract)):
                        list_of_mark_of_subject_of_control.append(mark + pract)
                    elif mark is pd.NA or pd.isna(mark):
                        list_of_mark_of_subject_of_control.append(pract)
                    elif pract is pd.NA or pd.isna(pract):
                        list_of_mark_of_subject_of_control.append(mark)
                    else:
                        list_of_mark_of_subject_of_control.append(0)
                elif 'Письменный ответ' in temp_list_of_subj:
                    mark = temp_list_of_mark[temp_list_of_subj.index('Работа на учебной встрече')]
                    pract = temp_list_of_mark[temp_list_of_subj.index('Письменный ответ')]
                    if (mark is not pd.NA and pract is not pd.NA) and (not pd.isna(mark) and not pd.isna(pract)):
                        list_of_mark_of_subject_of_control.append(mark + pract)
                    elif mark is pd.NA or pd.isna(mark):
                        list_of_mark_of_subject_of_control.append(pract)
                    elif pract is pd.NA or pd.isna(pract):
                        list_of_mark_of_subject_of_control.append(mark)
                    else:
                        list_of_mark_of_subject_of_control.append(0)
                else:
                    list_of_mark_of_subject_of_control.append(
                        temp_list_of_mark[temp_list_of_subj.index('Работа на учебной встрече')])
                # print(temp_list_of_subj)
                # if temp_list_of_mark[temp_list_of_subj.index('Работа на учебной встрече')] is None or math.isnan(
                #         temp_list_of_mark[temp_list_of_subj.index('Работа на учебной встрече')]):
                #     print(temp_list_of_mark[temp_list_of_subj.index('Практическое задание')])
                #     print(temp_list_of_mark[temp_list_of_subj.index('Работа на учебной встрече')])
                #     print(type(temp_list_of_mark[temp_list_of_subj.index('Работа на учебной встрече')]))
                #     print(temp_list_of_mark[temp_list_of_subj.index('Работа на учебной встрече')] is None)
                #     print(math.isnan(temp_list_of_mark[temp_list_of_subj.index('Работа на учебной встрече')]))
                #     list_of_mark_of_subject_of_control.append(
                #         temp_list_of_mark[temp_list_of_subj.index('Практическое задание')])
                # else:
                #     # print(temp_list_of_mark[temp_list_of_subj.index('Работа на учебной встрече')])
                # list_of_mark_of_subject_of_control.append(
                #     temp_list_of_mark[temp_list_of_subj.index('Работа на учебной встрече')])
                list_of_arrival.append(temp_list_of_mark[temp_list_of_subj.index('Посещение')])
                try:
                    list_of_test.append(str(temp_list_of_mark[temp_list_of_subj.index('Контрольная работа')]))
                except:
                    list_of_test.append('-1.0')

                list_of_result_points.append(last_row[7])
                list_of_result_mark.append(last_row[8])
                # list_of_stud_email.append(last_row[9])
                # list_of_stud_course.append(last_row[10])
                list_of_teachers.append(last_row[9])

                temp_list_of_subj.clear()
                temp_list_of_mark.clear()

                temp_list_of_subj.append(row[5])
                temp_list_of_mark.append(row[6])
                last_row = row
        else:
            temp_list_of_subj.append(row[5])
            temp_list_of_mark.append(row[6])
            last_row = row
    df_list = [list_of_rmup, list_of_rmup_link, list_of_stud_fio, list_of_team, list_of_name_of_lesson,
               list_of_mark_of_subject_of_control, list_of_arrival, list_of_test, list_of_result_points,
               list_of_result_mark, list_of_teachers]

    df_true = pd.DataFrame(df_list)
    df_true = df_true.T
    df_true.to_csv(index=False, path_or_buf='/backend/scripts/df_test.csv', sep="_", header=False)

    df_real = pd.read_csv('/backend/scripts/df_test.csv', delimiter='_', header=None)

    print(df_real.columns)
    df_real.columns = df_real.columns.astype(str)

    db = connect_db_data_old()

    unique_values_rmup_table = df_real[['0', '1']].drop_duplicates().values.tolist()
    names = [row[0] for row in unique_values_rmup_table]
    links = [row[1] for row in unique_values_rmup_table]
    unique_values_rmup_table = [names, links]
    print(unique_values_rmup_table)
    for name, link in zip(unique_values_rmup_table[0], unique_values_rmup_table[1]):
        db.add(Rmup(name=name, link=link, date_of_add=datetime.datetime.now().date()))
    db.commit()
    unique_values_stud_table = df_real['2'].drop_duplicates().values.tolist()
    print(unique_values_stud_table)
    for name in unique_values_stud_table:
        db.add(Stud(name=name, email='null', speciality='null', date_of_add=datetime.datetime.now().date()))
    db.commit()

    unique_values_team_table = df_real[['0', '1', '3']].drop_duplicates().values.tolist()
    print(unique_values_team_table)
    names = [row[0] for row in unique_values_team_table]
    links = [row[1] for row in unique_values_team_table]
    stud_names = [row[2] for row in unique_values_team_table]
    unique_values_team_table = [names, links, stud_names]
    for name, link, stud_name in zip(unique_values_team_table[0], unique_values_team_table[1],
                                     unique_values_team_table[2]):
        rmup_id = db.query(Rmup.id).filter(Rmup.name == name).first()
        db.add(Team(name=stud_name, rmup_id=rmup_id[0], date_of_add=datetime.datetime.now().date()))
    db.commit()

    # todo этот массив надо будет разбивать в случае практики по запятой или не нужно кстати
    unique_values_teacher_table = df_real['10'].drop_duplicates().values.tolist()
    print(unique_values_teacher_table)
    for name in unique_values_teacher_table:
        db.add(Teacher(name=name, lect_or_pract='', date_of_add=datetime.datetime.now().date()))
    db.commit()
    previous_name = ''
    counter = 0
    # todo сделать кучу секций под каждую команду
    for rmup_name, rmup_link, stud_name, team, name_of_lesson, mark, arrival1, test1, result_points1, result_mark1, teacher_name in zip(
            df_real['0'], df_real['1'], df_real['2'], df_real['3'], df_real['4'], df_real['5'], df_real['6'],
            df_real['7'],
            df_real['8'], df_real['9'], df_real['10']):
        name = name_of_lesson
        if name in previous_name:
            name += str(counter)
            counter += 1
        else:
            name += str(0)
            counter = 1
        if math.isnan(mark):
            mark_for_work = 0
        else:
            mark_for_work = mark
        if arrival1 is None:
            arrival = "Н"
        else:
            try:
                if math.isnan(arrival1):
                    arrival = "Н"
            except:
                arrival = arrival1
        if math.isnan(test1):
            test = -0.00000000001
        elif int(test1) == -1:
            test = -0.00000000001
        else:
            test = test1

        result_points = result_points1
        result_mark = result_mark1
        stud_id = db.query(Stud.id).filter(Stud.name == stud_name).first()[0]
        team_id = db.query(Team.id).filter(Team.name == team).first()[0]
        teacher_id = db.query(Teacher.id).filter(Teacher.name == teacher_name).first()[0]
        db.add(Lesson(name=name, mark_for_work=mark_for_work, arrival=arrival, test=test, result_points=result_points,
                      result_mark=result_mark, stud_id=stud_id, team_id=team_id, teacher_id=teacher_id,
                      date_of_add=datetime.datetime.now().date()))
        previous_name = name
    db.commit()
    db.close()
# name ='Иностранный язык: английский (средний уровень I)'
# etl(rmup_name = name)
etl()
