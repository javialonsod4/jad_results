import mysql.connector
import boto3
import subprocess

# Conectarse a la instancia EC2 via SSH
client = boto3.client('ec2', region_name='us-east-1')
instances = client.describe_instances(
    Filters=[
        {
            'Name': 'tag:Name',
            'Values': ['jad2']
        },
    ]
)
instance_id = instances['Reservations'][0]['Instances'][0]['InstanceId']

# Ejecutar el comando en la instancia EC2
session = boto3.Session()
ssh = session.create_connection(
    host=instance_id,
    key_filename='C:/Users/javia/jad-results/vockey.pem',
    command='bash /home/ec2-user/jad-results/pr4.sh'
)
stdin, stdout, stderr = ssh.exec_command('bash /home/ec2-user/jad-results/pr4.sh')
print(stdout.read())

mydb = mysql.connector.connect(
  host="jaddb.cmtu6ejlnowu.us-east-1.rds.amazonaws.com",
  user="admin",
  password="jaddb-password",
  database="jaddb"
)

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM victorias")

for x in mycursor:
  print(x)