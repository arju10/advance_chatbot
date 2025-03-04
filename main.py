from fastapi import FastAPI
from db.db import create_connection, create_table


app = FastAPI()

create_connection()
# Create table (if it doesn't exist)
create_table()