import pandas as pd
import mysql.connector

# Conectar a la base de datos RDS "jaddb"
mydb = mysql.connector.connect(
  host="jaddb.cmtu6ejlnowu.us-east-1.rds.amazonaws.com",
  user="admin",
  password="jaddb-password",
  database="jaddb"
)

# Leer el archivo CSV que se añade al bucket "jad-football-results" de S3
df = pd.read_csv('s3://jad-football-results/results.csv')

# Estos comandos crearán nuevas columnas que pueden ser útiles para futuras consultas
# Las columnas son si ha ganado el local, el visitante, o si ha habido empate (result),
# el equipo ganador o empate (winner) y el equipo perdedor o empate (loser)
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

# Crear la tabla "mas_victorias" si no existe
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS mas_victorias (equipo VARCHAR(255), victorias INT);")

# Insertar los datos en la tabla
for index, row in df.iterrows():
    # Seleccionamos el país ganador, para los partidos que no son empates
    if row['winner'] != 'Draw':
        equipo = row['winner']
        sql = "INSERT INTO mas_victorias (equipo, victorias) VALUES (%s, 1);"
        val = (equipo)
        mycursor.execute(sql, val)

# Sumamos las victorias de cada selección y ordenamos la tabla en orden descendente
# de victorias.
mycursor.execute("SELECT equipo, COUNT(*) AS total_victorias"\
                 "FROM mas_victorias"\
                 "GROUP BY equipo"\
                 "ORDER BY total_victorias DESC;")

# Confirmamos los cambios.
mydb.commit()

# Cerramos la conexión
mycursor.close()
mydb.close()
