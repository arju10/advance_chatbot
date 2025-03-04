from fastapi import FastAPI
from db.db import create_connection


app = FastAPI()

create_connection()
