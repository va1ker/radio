from dotenv import load_dotenv, find_dotenv
import os
import psycopg2
from time import sleep

load_dotenv(find_dotenv())
# Check connect to Postgres
for i in range(5):
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get("POSTGRES_DB"),
            user=os.environ.get("POSTGRES_USER"),
            password=os.environ.get("POSTGRES_PASSWORD"),
        )
        print("\nConnected!\n")
        conn.close()
        sleep(3)
    except:
        print("\n My dog fucked up\n")
