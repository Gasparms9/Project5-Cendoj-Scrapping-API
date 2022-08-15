import sqlalchemy as alch
import os
import dotenv
import pandas as pd
import mysql.connector

dotenv.load_dotenv()

## gives us the sql connection
passw = os.getenv("pass_sql")
dbName = "sentencias_españa"
connectionData = f"mysql+pymysql://root:{passw}@localhost/{dbName}"
engine = alch.create_engine(connectionData)



