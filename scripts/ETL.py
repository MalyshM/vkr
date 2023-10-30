import datetime
import hashlib
import pickle

import pandas as pd
import os

# Specify the path to the Excel file
import sqlalchemy

from app.models import connect_db, Student, TableForAll

file_path = 'dataframe.csv'
df = pd.read_csv(file_path, delimiter=';')
# df = df.fillna(0)
# pd.set_option('display.max_columns', None)
print(df.head())
print(df.dtypes)
previous = ''
anonymized_dict = {}
for column_name, column_data in df.items():
    print(column_name, end="\n name\n")
    # print(column_data)
    print(column_data.isna().sum(), end="\n сумма nan\n")
    if column_name == "ФИО студента":
        df[column_name] = df[column_name].apply(
            lambda x: anonymized_dict.setdefault(x, hashlib.sha256(x.encode()).hexdigest()))
    if column_name == "Предмет контроля":
        print(column_data.value_counts(), end="\n Предмет контроля\n")
    if column_name == "Итоговая оценка":
        df[column_name] = column_data.fillna("Отчислено")
        print(df[column_name].isna().sum(), end="\n сумма nan Итоговая оценка\n")
    if column_name == "Оценка за предметы контроля":
        # df[column_name] = column_data.fillna("Отчислено")
        print(previous, end="\n previous\n")
        # df[column_name] = df[[column_name, previous]].apply(lambda x: print(x[0]))
        df[column_name] = df[[column_name, previous]].apply(
            lambda x: 0.0 if pd.isna(x[column_name]) and (
                    x[previous] == "Работа на учебной встрече" or x[previous] == "Контрольная работа")
            else x[column_name], axis=1)
        df[column_name] = df[[column_name, previous]].apply(
            lambda x: "Н" if pd.isna(x[column_name]) and (
                    x[previous] == "Посещение")
            else x[column_name], axis=1)
        print(df[column_name].isna().sum(), end="\n df[column_name].isna().sum()\n")
    previous = column_name
# print(anonymized_dict)
# with open("anonymized_dict.pkl", "wb") as file:
#     pickle.dump(anonymized_dict, file)
# with open("anonymized_dict.pkl", "rb") as file:
#     anonymized_dict= pickle.load(file)
# print(anonymized_dict)
df.to_csv(index=False, path_or_buf='asd.csv', sep="_", header=False)
file_path = 'E.csv'
df_without_na = pd.read_csv(file_path, delimiter='_', header=None)
db = connect_db()
for index, row in df_without_na.iterrows():
    # print(row)

    db.add(TableForAll(name_of_subject=row[0], link_of_subject=row[1], name_of_student=row[2], team=row[3],
                       name_of_meeting=row[4], subject_of_control=row[5], mark_of_subject_of_control=row[6],
                       result_points=row[7], result_mark=row[8], date_of_add=datetime.datetime.now().date()))
db.commit()
db.close()
