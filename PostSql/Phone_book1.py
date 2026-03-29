import psycopg2
import csv

from connect import get_connection


def create_tables():
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("""CREATE TABLE phone(
                ID SERIAL PRIMARY KEY,
                Name Varchar(128) NOT NULL,
                PhoneNum Varchar(128) NOT NULL)""")
    conn.commit()
    cur.close()
    conn.close()

def insert_csvdata(filename):
    conn=get_connection()
    cur=conn.cursor()
    with open(filename,encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("INSERT INTO phone (Name,PhoneNum) Values(%s,%s)",
                        (row["name"],row["phone"]))
    conn.commit()
    cur.close()
    conn.close()
def insert_contact(name, phone):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO phone (Name, PhoneNum) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()

    cur.close()
    conn.close()
def show_contacts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phone")

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()    
def search_contact(name):
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("SELECT * FROM phone WHERE Name=%s",
                (name,))
    result=cur.fetchall()
    for res in result:
        print(res)

    cur.close()
    conn.close()
def update_phone(name,phone):
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("UPDATE phone SET PhoneNum=%s WHERE Name=%s",
                (phone,name))
    conn.commit()

    cur.close()
    conn.close()

def delete_name(name):
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("DELETE FROM phone WHERE Name=%s",
                (name,))
    
    conn.commit()

    cur.close()
    conn.close()
    

def delete_phone(phone):
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("DELETE FROM phone WHERE PhoneNum=%s",
                (phone,))
    conn.commit()

    cur.close()
    conn.close()

if __name__=="__main__":
    create_tables()
    insert_csvdata("contacts.csv")
    insert_contact("Arman", "87009998877")

    print("\nВсе контакты:")
    show_contacts()

    print("\nПоиск:")
    search_contact("Aliaskar")

    update_phone("Aliaskar", "87001112233")

    delete_phone("870000000")


    
