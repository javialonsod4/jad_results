import pandas as pd

import boto3

s3 = boto3.client('s3')

bucket_name = 'jad-resultados-big-data'
object_key = 'results.csv'

# Descargar el archivo a un objeto en memoria
response = s3.get_object(Bucket=bucket_name, Key=object_key)
data = response['Body'].read().decode('utf-8')

# Crear un DataFrame de pandas a partir del contenido
df = pd.read_csv(io.StringIO(data))


#data = pd.read_csv('data/results.csv', sep=',')
print('Primeras filas:\n', df.head())
print('\nNombre de las columnas:\n', df.columns)

print('\nValores nulos:\n', df.isnull().sum())

result_list = []
winner_list = []
loser_list = []

for local_team, visit_team, goals_l, goals_v in zip(data['home_team'], data['away_team'],
                                                   data['home_score'], data['away_score']):
    if goals_l > goals_v:
        result_list.append('Home win')
        winner_list.append(local_team)
        loser_list.append(visit_team)
    elif goals_l == goals_v:
        result_list.append('Draw')
        winner_list.append('Draw')
        loser_list.append('Draw')
    else:
        result_list.append('Away win')
        winner_list.append(visit_team)
        loser_list.append(local_team)

df['result'] = result_list
df['winner'] = winner_list
df['loser'] = loser_list

print('\nPrimeras filas:\n', df.head())