import psycopg2
from config import load_config

def get_connection():
    config = load_config()

    conn = psycopg2.connect(
        host=config["host"],
        database=config["database"],
        user=config["user"],
        password=config["password"]
    )

    return conn