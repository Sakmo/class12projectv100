import mysql.connector
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import barcode
import tkinter as tk
from tkinter import messagebox


db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root"
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

def add_record(connection, table_name, admno, name, late_count):
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

def delete_record(admno, connection, table_name):
    cursor = connection.cursor()
    select_query = f"SELECT admno FROM {table_name}"
    cursor.execute(select_query)
    valid_admno_list = [record[0] for record in cursor.fetchall()]
    
    if admno in valid_admno_list:
        delete_query = f"DELETE FROM {table_name} WHERE admno = %s"
        cursor.execute(delete_query, (admno,))
        connection.commit()
        cursor.close()
        print("succ")
        return False
    else:
        cursor.close()
        print("nope")
        return True
    

def display_records(connection, table_name, choice):
    cursor = connection.cursor()
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
                messagebox.showinfo("Records Displayed", "Filtered records displayed in console.")
                print("=" * 30)
        if len(records)==0:
            messagebox.showinfo("No Records Found")
        cursor.close()
    else:
        messagebox.showinfo("Invalid Input", "Please check your input.")


def report(connection, table_name, adm_num):

    # admno = barcode.scan()
    admno = adm_num
    if admno == None:
        admno = barcode.scan()
        if admno == 0:
            messagebox.showinfo("Invalid Input", "Invalid Input")
            return
    else:
        pass
    
    cursor = connection.cursor()
    select_query = f"SELECT admno FROM {table_name}"
    cursor.execute(select_query)
    valid_admno_list = [record[0] for record in cursor.fetchall()]
    
    if admno in valid_admno_list:
        cursor.execute(f"SELECT late_count FROM {table_name} where admno = {admno}")
        count_init = cursor.fetchall()[0][0]
        query = f"UPDATE {table_name} SET late_count = late_count + 1 where admno = {admno}"
        cursor.execute(query)
        connection.commit()
        messagebox.showinfo("Latecomer Reported", f"Count: {count_init} ----> {count_init+1}")
    else:
        messagebox.showinfo("Admission Number not found", "Admission Number not found")
    
    cursor.close()


def main():
    connection = mysql.connector.connect(**db_config)
    database_name = "latecomers"
    table_name = "students"

    create_database(connection, database_name)
    connection.database = database_name
    create_table(connection, table_name)


    # Function to handle the "Add Record" button
    def open_add_record():
        page1 = tk.Toplevel(root)
        page1.title("Add Record")
        page1.geometry("400x400")
        
        # Add content and widgets for adding a record
        tk.Label(page1, text="Add a New Record", font=("Helvetica", 18, "bold")).pack(pady=10)
        tk.Label(page1, text="Name:").pack()
        name_entry = tk.Entry(page1)
        name_entry.pack()
        tk.Label(page1, text="Admission No:").pack()
        admno_entry = tk.Entry(page1)
        admno_entry.pack()
        tk.Label(page1, text="Late Count:").pack()
        latecount_entry = tk.Entry(page1)
        latecount_entry.pack()
        
        def submit_record():
            name = name_entry.get()
            admno = int(admno_entry.get())
            late_count = latecount_entry.get()
            print(name, admno, late_count)
            add_record(connection, table_name, admno, name, late_count)
            messagebox.showinfo("Record Added", "Record added successfully!")
            page1.destroy()
        
        submit_button = tk.Button(page1, text="Submit", command=submit_record)
        submit_button.pack(pady=10)

    # Function to handle the "Delete Record" button
    def open_delete_record():
        page2 = tk.Toplevel(root)
        page2.title("Delete Record")
        page2.geometry("400x400")
        
        tk.Label(page2, text="Delete a Record", font=("Helvetica", 18, "bold")).pack(pady=10)
        tk.Label(page2, text="Enter Admission Number to Delete:").pack()
        id_entry = tk.Entry(page2)
        id_entry.pack()
        
        def del_record():
            admno = int(id_entry.get())
            err = delete_record(admno, connection, table_name)
            # You can handle the record deletion logic here
            if err:
                messagebox.showinfo("No record found", "Invalid Admission Number")
            else:
                messagebox.showinfo("Record Deleted", "Record deleted successfully!")
  
            page2.destroy()
        
        submit_button = tk.Button(page2, text="Delete", command=del_record)
        submit_button.pack(pady=10)

    # Function to handle the "Display Records" button
    def open_display_records():
        page3 = tk.Toplevel(root)
        page3.title("Display Records")
        page3.geometry("400x400")
        
        # Add content and widgets for displaying records
        tk.Label(page3, text="Display Records", font=("Helvetica", 18, "bold")).pack(pady=10)
        tk.Label(page3, text="Enter Your Query WHERE admno").pack()
        q = tk.Entry(page3)
        q.pack()
        
        def show_recs():
            query = q.get()
            display_records(connection, table_name, query)
            page3.destroy()
        
        submit_button = tk.Button(page3, text="Display", command=show_recs)
        submit_button.pack(pady=10)

    # Function to handle the "Report Latecomer" button
    def open_report_latecomer():
        page4 = tk.Toplevel(root)
        page4.title("Report Latecomer")
        page4.geometry("400x400")
        
        # Add content and widgets for reporting a latecomer
        tk.Label(page4, text="Report Latecomer", font=("Helvetica", 18, "bold")).pack(pady=10)
        tk.Label(page4, text="Admission Number of Latecomer (leave empty to scan)").pack()
        a = tk.Entry(page4)
        a.pack()
        
        def report_latecomer():
            if a.get() == '':
                adm_num = None
                report(connection, table_name, adm_num)
            else:
                adm_num = int(a.get())
                report(connection, table_name, adm_num)


            page4.destroy()
        
        submit_button = tk.Button(page4, text="Report", command=report_latecomer)
        submit_button.pack(pady=10)

    # Main window
    root = tk.Tk()
    root.title("Record Management System")
    root.geometry("600x600")

    # Create and place buttons for different actions
    tk.Label(root, text="Student Latecomer Database", font=("Helvetica", 24, "bold")).pack(pady=20)
    add_button = tk.Button(root, text="Add Record", command=open_add_record, font=("Helvetica", 12, "bold"))
    delete_button = tk.Button(root, text="Delete Record", command=open_delete_record, font=("Helvetica", 12, "bold"))
    display_button = tk.Button(root, text="Display Records", command=open_display_records, font=("Helvetica", 12, "bold"))
    report_button = tk.Button(root, text="Report Latecomer", command=open_report_latecomer, font=("Helvetica", 12, "bold"))
    exit_button = tk.Button(root, text="Exit", command=root.destroy, font=("Helvetica", 12, "bold"))

    add_button.pack()
    delete_button.pack()
    display_button.pack()
    report_button.pack()
    exit_button.pack(pady=20)

    root.mainloop()

    connection.close()

main()
    

