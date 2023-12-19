import datetime
import hashlib
import math
import pickle

import pandas as pd
import os

# Specify the path to the Excel file
import sqlalchemy

from models import *

file_path = '/backend/backend/scripts/dataframe.csv'
df = pd.read_csv(file_path, delimiter=';')
df_teachers = pd.read_csv('/backend/backend/scripts/teachers.csv', delimiter=';',
                          names=['1', '2', 'Команда', '3', 'лектор', 'практик'])
# df = df.fillna(0)
# pd.set_option('display.max_columns', None)
print(df.head())
print(df.dtypes)
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
list_of_teachers = []

temp_list_of_subj = []
temp_list_of_mark = []

df["ФИО студента"] = df["ФИО студента"].apply(
    lambda x: anonymized_dict.setdefault(x, hashlib.sha256(x.encode()).hexdigest()))
with open("/backend/backend/scripts/anonymized_dict.pkl", "wb") as file:
    pickle.dump(anonymized_dict, file)


def find_teacher(row):
    if 'Л' in row['Команда']:
        teacher_type = 'лектор'
    else:
        teacher_type = 'практик'

    teacher_row = df_teachers[df_teachers['Команда'] == row['Команда']]
    for index, row in teacher_row.iterrows():
        if 'лектор' == teacher_type:
            # print(row[-1])
            return row[-1]
        else:
            # print(row[-2])
            return row[-2]


df['Преподаватель'] = df.apply(find_teacher, axis=1)
print(df['Преподаватель'])
print(df.columns)
for index, row in df.iterrows():
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

            list_of_mark_of_subject_of_control.append(
                temp_list_of_mark[temp_list_of_subj.index('Работа на учебной встрече')])
            list_of_arrival.append(temp_list_of_mark[temp_list_of_subj.index('Посещение')])
            list_of_test.append(temp_list_of_mark[temp_list_of_subj.index('Контрольная работа')])

            list_of_result_points.append(row[7])
            list_of_result_mark.append(row[8])
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

            list_of_mark_of_subject_of_control.append(
                temp_list_of_mark[temp_list_of_subj.index('Работа на учебной встрече')])
            list_of_arrival.append(temp_list_of_mark[temp_list_of_subj.index('Посещение')])
            try:
                list_of_test.append(temp_list_of_mark[temp_list_of_subj.index('Контрольная работа')])
            except:
                list_of_test.append(math.nan)

            list_of_result_points.append(last_row[7])
            list_of_result_mark.append(last_row[8])
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

df_true.to_csv(index=False, path_or_buf='/backend/backend/scripts/df_true.csv', sep="_", header=False)

df_real = pd.read_csv('/backend/backend/scripts/df_true.csv', delimiter='_', header=None)

print(df_real.columns)
df_real.columns = df_real.columns.astype(str)

db = connect_db_data()

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
    db.add(Stud(name=name, email='', speciality='', date_of_add=datetime.datetime.now().date()))
db.commit()

unique_values_team_table = df_real[['0', '1', '3']].drop_duplicates().values.tolist()
print(unique_values_team_table)
names = [row[0] for row in unique_values_team_table]
links = [row[1] for row in unique_values_team_table]
stud_names = [row[2] for row in unique_values_team_table]
unique_values_team_table = [names, links, stud_names]
for name, link, stud_name in zip(unique_values_team_table[0], unique_values_team_table[1], unique_values_team_table[2]):
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
counter = 1
# todo сделать кучу секций под каждую команду
for rmup_name, rmup_link, stud_name, team, name_of_lesson, mark, arrival1, test1, result_points1, result_mark1, teacher_name in zip(
        df_real['0'], df_real['1'], df_real['2'], df_real['3'], df_real['4'], df_real['5'], df_real['6'], df_real['7'],
        df_real['8'], df_real['9'], df_real['10']):
    name = name_of_lesson
    if name in previous_name:
        name += str(counter)
        counter += 1
    else:
        counter = 1
    if math.isnan(mark):
        mark_for_work = 0
    else:
        mark_for_work = mark
    if arrival1 is None:
        arrival = "Н"
    else:
        arrival = arrival1
    if math.isnan(test1):
        test = 0
    else:
        test = test1

    result_points = result_points1
    result_mark = result_mark1
    stud_id = db.query(Stud.id).filter(Stud.name == stud_name).first()[0]
    # вот team_id доработать чтоб еще по rmup чекалось чтоб не обосраться
    team_id = db.query(Team.id).filter(Team.name == team).first()[0]
    teacher_id = db.query(Teacher.id).filter(Teacher.name == teacher_name).first()[0]
    db.add(Lesson(name=name, mark_for_work=mark_for_work, arrival=arrival, test=test, result_points=result_points,
                  result_mark=result_mark, stud_id=stud_id, team_id=team_id, teacher_id=teacher_id,
                  date_of_add=datetime.datetime.now().date()))
    previous_name = name
db.commit()
db.close()
# for index, row in df_real.iterrows():

# for column_name, column_data in df.items():
#     print(column_name, end="\n name\n")
#     # print(column_data)
#     print(column_data.isna().sum(), end="\n сумма nan\n")
#     if column_name == "ФИО студента":
#         df[column_name] = df[column_name].apply(
#             lambda x: anonymized_dict.setdefault(x, hashlib.sha256(x.encode()).hexdigest()))
#     if column_name == "Предмет контроля":
#         print(column_data.value_counts(), end="\n Предмет контроля\n")
#     if column_name == "Итоговая оценка":
#         df[column_name] = column_data.fillna("Отчислено")
#         print(df[column_name].isna().sum(), end="\n сумма nan Итоговая оценка\n")
#     if column_name == "Оценка за предметы контроля":
#         # df[column_name] = column_data.fillna("Отчислено")
#         print(previous, end="\n previous\n")
#         # df[column_name] = df[[column_name, previous]].apply(lambda x: print(x[0]))
#         df[column_name] = df[[column_name, previous]].apply(
#             lambda x: 0.0 if pd.isna(x[column_name]) and (
#                     x[previous] == "Работа на учебной встрече" or x[previous] == "Контрольная работа")
#             else x[column_name], axis=1)
#         df[column_name] = df[[column_name, previous]].apply(
#             lambda x: "Н" if pd.isna(x[column_name]) and (
#                     x[previous] == "Посещение")
#             else x[column_name], axis=1)
#         print(df[column_name].isna().sum(), end="\n df[column_name].isna().sum()\n")
#     previous = column_name
# print(anonymized_dict)
# with open("anonymized_dict.pkl", "wb") as file:
#     pickle.dump(anonymized_dict, file)
# with open("anonymized_dict.pkl", "rb") as file:
#     anonymized_dict= pickle.load(file)
# print(anonymized_dict)
# df.to_csv(index=False, path_or_buf='asd.csv', sep="_", header=False)
# file_path = 'asd.csv'
# df_without_na = pd.read_csv(file_path, delimiter='_', header=None)
# db = connect_db()
# for index, row in df_without_na.iterrows():
#     # print(row)
#
#     db.add(TableForAll(name_of_subject=row[0], link_of_subject=row[1], name_of_student=row[2], team=row[3],
#                        name_of_meeting=row[4], subject_of_control=row[5], mark_of_subject_of_control=row[6],
#                        result_points=row[7], result_mark=row[8], date_of_add=datetime.datetime.now().date()))
# db.commit()
# db.close()
