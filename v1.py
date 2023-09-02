import mysql.connector
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import barcode
import warnings

warnings.filterwarnings('ignore')

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "vatsal"
}

def create_database(connection, database_name):
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    cursor.close()

def create_table(connection, table_name):
    cursor = connection.cursor()
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

def add_record(connection, table_name):
    admno = int(input("Enter Admno: "))
    name = input("Enter Name: ")
    late_count = int(input("Enter Late Count: "))
    #photo_path = input("Enter Photo Path: ")
    photo_data = 'pfp/'+('0000'+str(admno))[-5:]+'.png'

    #with open(photo_path, "rb") as photo_file:
        #photo_data = photo_file.read()

    cursor = connection.cursor()
    insert_query = f"INSERT INTO {table_name} (admno, name, late_count, photo) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_query, (admno, name, late_count, photo_data))
    connection.commit()
    cursor.close()
    print("Record added successfully!")

def delete_record(connection, table_name):
    admno = int(input("Enter Admno to delete: "))
    
    cursor = connection.cursor()
    select_query = f"SELECT admno FROM {table_name}"
    cursor.execute(select_query)
    valid_admno_list = [record[0] for record in cursor.fetchall()]
    
    if admno in valid_admno_list:
        delete_query = f"DELETE FROM {table_name} WHERE admno = %s"
        cursor.execute(delete_query, (admno,))
        connection.commit()
        print("Record deleted successfully!")
    else:
        print("Invalid admission number. No record found for deletion.")
    
    cursor.close()

def display_records(connection, table_name):
    cursor = connection.cursor()
    choice = input('Enter clause:\n admno')   # 1) <40, 2) >50, 3)=90, 4)all, 5) scan
    if choice[0] in '<>':
        select_query = f"SELECT * FROM {table_name} where admno {choice}"
        cursor.execute(select_query)
        records = cursor.fetchall()
        print('Admno','Name','Late Count', sep='\t')
        for record in records:
            print(record[0],record[1],record[2], sep='\t')
        if len(records)==0:
            print('No records found')
        cursor.close()
    elif choice=='all':
        select_query = f"SELECT * FROM {table_name}"
        cursor.execute(select_query)
        records = cursor.fetchall()
        print('Admno','Name','Late Count', sep='\t')
        for record in records:
            print(record[0],record[1],record[2], sep='\t')
        if len(records)==0:
            print('No records found')
        cursor.close()
    elif choice[0] == '=' or choice=='scan':
        if choice=='scan':
            choice = '='+str(barcode.scan())

        select_query = f"SELECT * FROM {table_name} where admno {choice}"
        cursor.execute(select_query)
        records = cursor.fetchall()
        for record in records:
            print("Admno:", record[0])
            print("Name:", record[1])
            print("Late Count:", record[2])
            print("Photo Data:", record[3])
            try:
                image = mpimg.imread(record[3])
                plt.imshow(image)
                plt.show()
            except:
                print('Invalid Image')
            finally:
                print("=" * 30)
        if len(records)==0:
            print('No records found')
        cursor.close()
    else:
        print('Invalid input')


def report(connection, table_name):
    admno = int(input("Enter Admno: "))
    
    cursor = connection.cursor()
    select_query = f"SELECT admno FROM {table_name}"
    cursor.execute(select_query)
    valid_admno_list = [record[0] for record in cursor.fetchall()]
    
    if admno in valid_admno_list:
        query = f"UPDATE {table_name} SET late_count = late_count + 1 where admno = {admno}"
        cursor.execute(query, (admno,))
        connection.commit()
        print("Reported successfully!")
    else:
        print("Invalid admno")
    
    cursor.close()


def main():
    connection = mysql.connector.connect(**db_config)
    database_name = "latecomers"
    table_name = "students"

    create_database(connection, database_name)
    connection.database = database_name
    create_table(connection, table_name)

    while True:
        print("Menu:")
        print("1. Add Record")
        print("2. Delete Record")
        print("3. Display Records")
        print("4. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            add_record(connection, table_name)
        elif choice == 2:
            delete_record(connection, table_name)
        elif choice == 3:
            display_records(connection, table_name)
        elif choice == 4:
            break
        else:
            print("Invalid choice. Please choose a valid option.")

    connection.close()

main()
    
