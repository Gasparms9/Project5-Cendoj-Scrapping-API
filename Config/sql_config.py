import sqlalchemy as alch
import os
import dotenv
import pandas as pd
import mysql.connector

dotenv.load_dotenv()

## gives us the sql connection
passw = os.getenv("pass_sql")
dbName = "harrypotter"
connectionData = f"mysql+pymysql://root:{passw}@localhost/{dbName}"
engine = alch.create_engine(connectionData)
df = pd.read_csv(r"C:\Users\lenovo\Desktop\Project_4\Project-4\data\hp_script.csv", encoding="ISO-8859-1")
sample = df.sample(2)


