import psycopg2

from config import load_config

def get_connection():
    confa=load_config()
    conn=psycopg2.connect(
        host=confa["host"],
        database=confa["database"],
        user=confa["user"],
        password=confa["password"]
    )


    
    return conn