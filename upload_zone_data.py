import pandas as pd
from sqlalchemy import create_engine



# Database connection parameters
username = "nurhan"
password = "nurhan123"
host = "localhost"  
port = "5434"       
database = "green_taxi"

# Create the database URL
database_url = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"

# Create a SQLAlchemy engine
engine = create_engine(database_url)
print(engine.connect())

df=pd.read_csv('taxi_zone_lookup.csv')

df.to_sql('taxi_zone_lookup',con=engine)

print("done")