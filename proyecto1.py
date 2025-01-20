import pandas as pd
import mysql.connector

# Conectar a la base de datos RDS
mydb = mysql.connector.connect(
  host="tu_host_rds",
  user="tu_usuario",
  password="tu_password",
  database="tu_base_de_datos"
)

# Leer el archivo CSV desde S3 (ajusta la ruta y el bucket)
df = pd.read_csv('s3://mi-bucket/resultados_futbol.csv')

# Crear la tabla si no existe
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS victorias (equipo VARCHAR(255), victorias INT)")

# Insertar los datos en la tabla
for index, row in df.iterrows():
    equipo = row['equipo']
    victorias = row['victorias']
    sql = "INSERT INTO victorias (equipo, victorias) VALUES (%s, %s)"
    val = (equipo, victorias)
    mycursor.execute(sql, val)

mydb.commit()
print(mycursor.rowcount, "record inserted.")

'''
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
'''
