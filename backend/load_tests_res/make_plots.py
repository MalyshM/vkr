import pandas as pd
import matplotlib.pyplot as plt


def plot(**params):
    plt.figure(figsize=(8, 6))
    plt.plot(df_true.index, df_true[params['column1']], label=params['label1'])
    plt.plot(df_true.index, df_true[params['column2']], label=params['label2'])
    plt.xlabel('Index')
    plt.ylabel(params['ylabel'])
    plt.title(params['title'])
    plt.legend()
    plt.savefig(fname=params['title'])


df_old = pd.read_csv('example_stats_history.csv', delimiter=',')
df_new = pd.read_csv('example_stats_history_new.csv', delimiter=',')

df_true = pd.DataFrame()
df_true['df_old_user_count'] = df_old['User Count']
df_true['df_new_user_count'] = df_new['User Count']
df_true['df_old_Requests_s'] = df_old['Requests/s']
df_true['df_new_Requests_s'] = df_new['Requests/s']
df_true['df_old_Total Request Count'] = df_old['Total Request Count']
df_true['df_new_Total Request Count'] = df_new['Total Request Count']
df_true['df_old_Total Failure Count'] = df_old['Total Failure Count']
df_true['df_new_Total Failure Count'] = df_new['Total Failure Count']
df_true['df_old_Total Average Response Time'] = df_old['Total Average Response Time']
df_true['df_new_Total Average Response Time'] = df_new['Total Average Response Time']

plot(**{'column1': "df_old_user_count", 'column2': "df_new_user_count", "label1": "Old User Count",
          "label2": "New User Count", "ylabel": 'User Count', "title": 'Comparison of User Count'})
plot(**{'column1': "df_old_Requests_s", 'column2': "df_new_Requests_s", "label1": "Old Requests/s",
          "label2": "New Requests/s", "ylabel": 'Requests/s', "title": 'Comparison of Requests in s'})
plot(**{'column1': "df_old_Total Request Count", 'column2': "df_new_Total Request Count",
          "label1": "Old Total Request Count",
          "label2": "New Total Request Count", "ylabel": 'Total Request Count',
          "title": 'Comparison of Total Request Count'})
plot(**{'column1': "df_old_Total Failure Count", 'column2': "df_new_Total Failure Count",
          "label1": "Old Total Failure Count",
          "label2": "New Total Failure Count", "ylabel": 'Total Failure Count',
          "title": 'Comparison of Total Failure Count'})
plot(**{'column1': "df_old_Total Average Response Time", 'column2': "df_new_Total Average Response Time",
          "label1": "Old Total Average Response Time",
          "label2": "New Total Average Response Time", "ylabel": 'Total Average Response Time',
          "title": 'Comparison of Total Average Response Time'})
