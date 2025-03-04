from fastapi import FastAPI
from db.db import create_connection, create_table, insert_data_from_file


app = FastAPI()
# Path to your JSON file
data_file = './data/genzmarketing_cleaned_data.json'

create_connection()
# Create table (if it doesn't exist)
create_table()

# Insert the data from the JSON file into the database
insert_data_from_file(data_file)

@app.get("/")
def read_root():
    return {"message": "Data inserted from the JSON file successfully!"}