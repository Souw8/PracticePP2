import psycopg2

from connect import get_connection

def create_table():
    conn=get_connection()
    curr=conn.cursor()
    curr.execute(
        """CREATE TABLE Phone111(
        id SERIAL PRIMARY KEY,
        names VARCHAR(128) NOT NULL,
        phones VARCHAR(128) NOT NULL)"""
    )

    conn.commit()

    curr.close()
    conn.close()
def search(pattern):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(

        "SELECT * FROM search_phonebooks(%s)",

        (pattern,)

    )

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()
def pagination(p_limit,p_offset):
    conn=get_connection()
    curr=conn.cursor()
    curr.execute("" \
    "SELECT * FROM get_phonebook_paginated(%s,%s)",
    (p_limit,p_offset))

    rows=curr.fetchall()

    for row in rows:
        print(row)
    
    curr.close()
    conn.close()
def insert_odin(name,phone):
    conn=get_connection()
    curr=conn.cursor()
    curr.execute("" \
    "CALL upsert(%s,%s)",
    (name,phone))

    conn.commit()

    curr.close()
    conn.close()

def insert_mnogo(names,phones):
    conn=get_connection()
    curr=conn.cursor()
    curr.execute("" \
    "CALL insert_many_users(%s,%s)",
    (names,phones))

    conn.commit()

    curr.close()
    conn.close()
def delete_query(name):
    conn=get_connection()
    curr=conn.cursor()
    curr.execute("" \
    "CALL delete_user(%s)",
    (name,))

    conn.commit()

    curr.close()
    conn.close()

if __name__=="__main__":

    insert_odin("Ali", "87071234567")
    insert_odin("Nursultan", "87075554433")

    print("search")
    search("Ali")

    print("\npagination")
    pagination(5,0)

    print("\nbulk insert")
    insert_mnogo(

        ["Dias","Aruzhan","Bad"],

        ["87012223344","+77017778899","abc"]

    )

    print("\ndelete")
    delete_query("Dias")

