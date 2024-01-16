import datetime
import hashlib
import math
import pickle

import pandas as pd

# Specify the path to the Excel file
# todo убрать backend. до билда в докере
# todo сделать как было '/backend/backend/scripts/dataframe.csv' и ниже так же /backend/backend/scripts/ вот это добавить нужно
from models import *

file_path = '/backend/scripts/dataframe.csv'
df = pd.read_csv(file_path, delimiter=';')
df_teachers = pd.read_csv('/backend/scripts/teachers.csv', delimiter=';',
                          names=['1', '2', 'Команда', '3', 'лектор', 'практик'])
df_students = pd.read_csv('/backend/scripts/df_students.csv', delimiter=';',
                          names=['name', 'email', 'Направление'])
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
list_of_stud_email = []
list_of_stud_course = []
list_of_teachers = []

temp_list_of_subj = []
temp_list_of_mark = []


def find_stud(row):
    student_row = df_students[df_students['name'] == row['ФИО студента']]
    if student_row.empty:
        return [None, None]
    return student_row.iloc[0]['email'], student_row.iloc[0]['Направление']


df[['Email', 'Направление']] = df.apply(find_stud, axis=1, result_type='expand')
print(df[['Email', 'Направление']].head)
df["ФИО студента"] = df["ФИО студента"].apply(
    lambda x: anonymized_dict.setdefault(x, hashlib.sha256(x.encode()).hexdigest()))
with open("/backend/scripts/anonymized_dict.pkl", "wb") as file:
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
# Index(['Название РМУП', 'Ссылка на РМУП', 'ФИО студента', 'Команда',
#        'Название встречи', 'Предмет контроля', 'Оценка за предметы контроля',
#        'Итог ТУ', 'Итоговая оценка', 'Email', 'Направление', 'Преподаватель'],
#       dtype='object')
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
            list_of_test.append(str(temp_list_of_mark[temp_list_of_subj.index('Контрольная работа')]))

            list_of_result_points.append(row[7])
            list_of_result_mark.append(row[8])
            list_of_stud_email.append(row[9])
            list_of_stud_course.append(row[10])
            list_of_teachers.append(row[11])

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
                list_of_test.append(str(temp_list_of_mark[temp_list_of_subj.index('Контрольная работа')]))
            except:
                list_of_test.append('-1.0')

            list_of_result_points.append(last_row[7])
            list_of_result_mark.append(last_row[8])
            list_of_stud_email.append(last_row[9])
            list_of_stud_course.append(last_row[10])
            list_of_teachers.append(last_row[11])

            temp_list_of_subj.clear()
            temp_list_of_mark.clear()

            temp_list_of_subj.append(row[5])
            temp_list_of_mark.append(row[6])
            last_row = row
    else:
        temp_list_of_subj.append(row[5])
        temp_list_of_mark.append(row[6])
        last_row = row
previous_name = '666666666666666'
counter = 1
for i, name in enumerate(list_of_name_of_lesson):
    if name == previous_name:
        list_of_name_of_lesson[i] = name + str(counter)
        counter += 1
    else:
        list_of_name_of_lesson[i] = name + str(0)
        counter = 1
    previous_name = name
# print(list_of_test)
list_of_test_sub = [item for item in list_of_test if float(item)>-0.5]
list_of_test_true = []
# list_of_test_sub.append('0.0')
# list_of_test_sub.append('0.0')
# list_of_test_sub.append('0.0')
print(len(list_of_test_sub))
print(len(list_of_name_of_lesson))
print(list_of_test_sub)
counter=0
for name in list_of_name_of_lesson:
    if name == 'Организация функций3' or name == 'Управляющие конструкции5' or name == 'Коллекции. Работа с файлами2':
        try:
            list_of_test_true.append(list_of_test_sub[0])
            list_of_test_sub=list_of_test_sub[1:]
        except:
            list_of_test_true.append('0.0')
        counter+=1
    else:
        list_of_test_true.append(math.nan)
        # list_of_test_sub = list_of_test_sub[1:]
print(counter)
df_list = [list_of_rmup, list_of_rmup_link, list_of_stud_fio, list_of_team, list_of_name_of_lesson,
           list_of_mark_of_subject_of_control, list_of_arrival, list_of_test_true, list_of_result_points,
           list_of_result_mark, list_of_stud_email, list_of_stud_course, list_of_teachers]


df_true = pd.DataFrame(df_list)
df_true = df_true.T
df_true.to_csv(index=False, path_or_buf='/backend/scripts/df_true.csv', sep="_", header=False)

df_real = pd.read_csv('/backend/scripts/df_true.csv', delimiter='_', header=None)

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
unique_values_stud_table = df_real[['2', '10', '11']].drop_duplicates().values.tolist()
print(unique_values_stud_table)
for name, email, speciality in unique_values_stud_table:
    db.add(Stud(name=name, email=email, speciality=speciality, date_of_add=datetime.datetime.now().date()))
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
unique_values_teacher_table = df_real['12'].drop_duplicates().values.tolist()
print(unique_values_teacher_table)
for name in unique_values_teacher_table:
    db.add(Teacher(name=name, lect_or_pract='', date_of_add=datetime.datetime.now().date()))
db.commit()
previous_name = ''
counter = 0
# todo сделать кучу секций под каждую команду
for rmup_name, rmup_link, stud_name, team, name_of_lesson, mark, arrival1, test1, result_points1, result_mark1, teacher_name in zip(
        df_real['0'], df_real['1'], df_real['2'], df_real['3'], df_real['4'], df_real['5'], df_real['6'], df_real['7'],
        df_real['8'], df_real['9'], df_real['12']):
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
        arrival = arrival1
    if math.isnan(test1):
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
