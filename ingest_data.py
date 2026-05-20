#!/usr/bin/env python
# coding: utf-8

import os
import argparse
from time import time
import pandas as pd
from sqlalchemy import create_engine
import requests
from tqdm import tqdm  # Need to ensure tqdm is installed in your env

def main(params):
    # 1. Retrieve arguments passed from the command line
    user = params.pg_user
    password = params.pg_pass
    host = params.pg_host 
    port = params.pg_port
    db = params.pg_db
    table_name = params.target_table
    url = params.url
    chunk_size = params.chunksize  # Now using the chunksize from arguments

    # Define the output filename
    csv_name = 'output.csv.gz'

    # 2. Download the CSV file
    print(f"Downloading data from {url}...")
    # verify=False skips SSL certificate verification (useful for some networks)
    response = requests.get(url, verify=False)
    with open(csv_name, 'wb') as f:
        f.write(response.content)
    print("Download finished!")

    # 3. Define schema / data types (Optimization)
    # Using Int64 for nullable integers and explicitly defining standard types
    taxi_dtypes = {
        "VendorID": "Int64",
        "passenger_count": "Int64",
        "trip_distance": "float64",
        "RatecodeID": "Int64",
        "store_and_fwd_flag": "string",
        "PULocationID": "Int64",
        "DOLocationID": "Int64",
        "payment_type": "Int64",
        "fare_amount": "float64",
        "extra": "float64",
        "mta_tax": "float64",
        "tip_amount": "float64",
        "tolls_amount": "float64",
        "improvement_surcharge": "float64",
        "total_amount": "float64",
        "congestion_surcharge": "float64"
    }
    # Columns to parse as datetime objects
    parse_dates = ["tpep_pickup_datetime", "tpep_dropoff_datetime"]

    # 4. Create Database Connection Engine
    # Note: 'host' will come from the --pg-host argument (e.g., 'my_postgres')
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # 5. Read data in chunks
    df_iter = pd.read_csv(
        csv_name, 
        iterator=True, 
        chunksize=chunk_size, 
        dtype=taxi_dtypes, 
        parse_dates=parse_dates
    )

    # Process the first chunk separately to handle table creation (replacement)
    try:
        df = next(df_iter)
        
        # Create the table (replace if exists) using the first chunk's schema
        df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
        
        # Insert the first chunk of data
        df.to_sql(name=table_name, con=engine, if_exists='append')
        print("Table initialized and first chunk inserted.")
    except StopIteration:
        print("Error: The downloaded file appears to be empty.")
        return

    # 6. Loop through the remaining chunks with tqdm progress bar
    # tqdm(df_iter) wraps the iterator to show a progress bar in the terminal
    count = 1 
    for df in tqdm(df_iter, desc="Processing chunks"):
        try:
            # Insert current chunk
            df.to_sql(name=table_name, con=engine, if_exists='append')
            count += 1
        except Exception as e:
            print(f"Error inserting chunk {count}: {e}")

    print(f"Successfully finished! Total chunks processed: {count}")

if __name__ == '__main__':
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    # Define all expected command-line arguments
    parser.add_argument('--pg-user', required=True, help='User name for postgres')
    parser.add_argument('--pg-pass', required=True, help='Password for postgres')
    parser.add_argument('--pg-host', required=True, help='Host for postgres')
    parser.add_argument('--pg-port', required=True, help='Port for postgres')
    parser.add_argument('--pg-db', required=True, help='Database name for postgres')
    parser.add_argument('--target-table', required=True, help='Name of the table for results')
    parser.add_argument('--url', required=True, help='URL of the CSV file')
    
    # Added chunksize argument with a default value, consistent with your docker run command
    parser.add_argument('--chunksize', type=int, default=100000, help='Batch size for data ingestion')

    # Parse arguments
    args = parser.parse_args()

    # Execute main function with parsed arguments
    main(args)