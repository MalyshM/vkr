import pandas as pd
import os

# Specify the path to the Excel file
import sqlalchemy

from app.models import connect_db, Student

file_path = 'test2.csv'
df = pd.read_csv(file_path, delimiter=';', header=None)
# df = df.fillna(0)
# pd.set_option('display.max_columns', None)
# print(df.head())
# print(df.dtypes)
names_of_lessons = [
    "2-1, 'Основные принципы организации Языка Python. Базовые элементы программирования и типы данных', Практическое занятие",
    "3-2, 'Основные принципы организации Языка Python. Базовые элементы программирования и типы данных', Практическое занятие",
    "4-3, 'Основные принципы организации Языка Python. Базовые элементы программирования и типы данных', Практическое занятие",
    "6-4, 'Управляющие конструкции', Практическое занятие",
    "7-5, 'Управляющие конструкции', Практическое занятие",
    "8-6, 'Управляющие конструкции', Практическое занятие",
    "9-7, 'Управляющие конструкции', Практическое занятие",
    "10-8, 'Управляющие конструкции', Практическое занятие",
    "11-9, 'Управляющие конструкции', Практическое занятие",
    "13-10, 'Организация функций', Практическое занятие",
    "14-11, 'Организация функций', Практическое занятие",
    "15-12, 'Организация функций', Практическое занятие",
    "16-13, 'Организация функций', Практическое занятие",
    "18-14, 'Работа со строками и текстом', Практическое занятие",
    "19-15, 'Работа со строками и текстом', Практическое занятие",
    "20-16, 'Работа со строками и текстом', Практическое занятие",
    "22-17, 'Коллекции. Работа с файлами', Практическое занятие",
    "23-18, 'Коллекции. Работа с файлами', Практическое занятие",
    "24-19, 'Коллекции. Работа с файлами', Практическое занятие",
    "26-20, 'Элементы функционального программирования', Практическое занятие",
    "27-21, 'Элементы функционального программирования', Практическое занятие",
    "31-1, 'Аттестация', Аттестация"
]
for column_name, column_data in df.items():
    if column_data.dtype == "float64":
        df[column_name] = column_data.fillna(0.0)
        # print(f"Column '{column_name}' is a float: NaN values filled with 0.0")
    elif column_data.dtype == "object":
        df[column_name] = column_data.fillna("Н")
        # print(f"Column '{column_name}' is an object: NaN values filled with 'Н'")

df.to_csv(index=False, path_or_buf='E.csv', sep="_",header=False)
file_path = 'E.csv'
df_without_na = pd.read_csv(file_path, delimiter='_', header=None)
db = connect_db()
for index, row in df_without_na.iterrows():
    # print(row)
    teams=row[3].split(',')
    if len(teams)>1:
        team_for_lectures=teams[0]
        team_for_practices=teams[1]
    else:
        team_for_practices = teams[0]
        team_for_lectures = sqlalchemy.sql.null()
    db.add(Student(name=row[0], email=row[1], speciality=row[2], team_for_lectures=team_for_lectures,
                   team_for_practices=team_for_practices))
db.commit()
db.close()
