import pandas as pd
from sqlalchemy import create_engine
import os

# 1. Connect Database
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

def ingest_data():
    # ----Ingest (CSV) ----
    print("Processing taxi_zone_lookup.csv...")
    df_zones = pd.read_csv('taxi_zone_lookup.csv')
    # Transfer to pg
    df_zones.to_sql(name='taxi_zone_lookup', con=engine, if_exists='replace', index=False)
    print("taxi zone data ingestion complete!")

    # ---- Processing Green Taxi Data (Parquet) ----
    print("Processing green_tripdata_2025-11.parquet...")
    # Pyarrow activated during parquet ingestion
    df_green = pd.read_parquet('green_tripdata_2025-11.parquet')
    
    # Ingest data to database
    df_green.to_sql(name='green_taxi_data', con=engine, if_exists='replace', index=False)
    print(f"Green Taxi Data Ingestion Complete， Total size: {len(df_green)} lines")

if __name__ == '__main__':
    ingest_data()