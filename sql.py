import mysql.connector
import csv

def detect_data_type(value):
    if value.isdigit():
        return "INT"
    try:
        float(value)
        return "FLOAT"
    except ValueError:
        return "VARCHAR(255)" 
conn = mysql.connector.connect(

    host = "localhost",
    user = "sayooj",
    password = "9895",
    database = "pc_parts"
)
cur = conn.cursor()

with open("csv_files/cpu.csv", "r") as file:
    reader = csv.reader(file)
    header = next(reader)
    sample_row = next(reader)

    column_types = [detect_data_type(value) if value is not None else "VARCHAR(255)" for value in sample_row]

    table_def = ", ".join(f"{header[i]} {column_types[i]}" for i in range(len(header)))

    create_tab = f"create table if not exists cpu (id int auto_increment primary key, {table_def})"

    insert = f"insert into cpu ({','.join(header)}) values({', '.join(['%s'] * len(header))})"

    cur.execute(create_tab)

    for row in reader:
        cur.execute(insert, row)

conn.commit()
print("csv data inserted successfully")

conn.close()