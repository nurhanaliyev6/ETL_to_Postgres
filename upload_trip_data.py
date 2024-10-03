import pandas as pd
from sqlalchemy import create_engine
import time



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


df_iter=pd.read_csv('green_tripdata_2019-09.csv',chunksize=50000,iterator=True)

df=next(df_iter)

df.lpep_pickup_datetime=pd.to_datetime(df.lpep_pickup_datetime)
df.lpep_dropoff_datetime=pd.to_datetime(df.lpep_dropoff_datetime)


df.head(0).to_sql("green_trip_data",con=engine)

try:
    while True:
        start_time = time.time()
        df=next(df_iter)

        df.lpep_pickup_datetime=pd.to_datetime(df.lpep_pickup_datetime)
        df.lpep_dropoff_datetime=pd.to_datetime(df.lpep_dropoff_datetime)


        df.to_sql("green_trip_data",con=engine,if_exists="append")
        print("--- %3s seconds ---" % (time.time() - start_time))



except Exception as e:
    print(f"No more addition: {e}")






