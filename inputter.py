import mysql.connector
import random
from names_dataset import NameDataset
nd = NameDataset()

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "vatsal"
}

connection = mysql.connector.connect(**db_config)

database_name = "latecomers"
table_name = "students"

connection.database = database_name
cursor = connection.cursor()
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
create_table_query = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    admno INT PRIMARY KEY NOT NULL,
    name VARCHAR(25),
    late_count INT,
    photo varchar(20)
)
"""

cursor.execute(create_table_query)
cursor.close()

lb = nd.get_top_names(n=254, country_alpha2='IN')['IN']['M']
lg = nd.get_top_names(n=254, country_alpha2='IN')['IN']['F']
l = lb+lg
random.shuffle(l)
#print(l)

for admno in range(501):
    late_count = random.randint(0,3)
    photo_data = 'pfp/'+('0000'+str(admno))[-5:]+'.png'
    name = l[admno]

    cursor = connection.cursor()
    insert_query = f"INSERT INTO {table_name} (admno, name, late_count, photo) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_query, (admno, name, late_count, photo_data))
    connection.commit()
    cursor.close()
    print(admno,end=',')