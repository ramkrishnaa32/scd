import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
import pandas as pd
from lib import constants
from datetime import datetime

# loading .env file
load_dotenv()

def get_engine():
    user = os.getenv("PG_USER")
    password = quote_plus(os.getenv("PG_PASSWORD"))
    port = os.getenv("PG_PORT")
    db = os.getenv("PG_DB")
    host = os.getenv("PG_HOST")
    connection_string = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
    engine = create_engine(connection_string)
    return engine

def read_table(engine, table_name):
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, engine)
    print(f"Completed reading, totalRecords: {len(df)}")
    return df

def load_to_postgres_transactional(df, table_name, engine, schema=None):
    """
    Load DataFrame to PostgreSQL within a transaction. Rolls back if any error occurs.
    Parameters:
        df (pd.DataFrame): Data to be loaded.
        table_name (str): Target table name.
        engine: SQLAlchemy engine.
        schema (str, optional): Schema name.
    """
    connection = engine.connect()
    trans = connection.begin()

    try:
        df.to_sql(
            name=table_name,
            con=connection,
            schema=schema,
            if_exists='append',
            index=False,
            method='multi',
            chunksize=1000
        )
        trans.commit()
        print(f"Successfully loaded {len(df)} records into {table_name}")
    except Exception as error:
        trans.rollback()
        print("Transaction rolled back due to error:", error)
    finally:
        connection.close()

def enhance_customers_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enhances the customer dataframe with surrogate key, effective/end dates, and active flag.
    Parameters:
        df (pd.DataFrame): The original customers DataFrame from Postgres.
    Returns:
        pd.DataFrame: Enhanced DataFrame with additional metadata columns.
    """
    
    df = df.copy()
    df['customer_skey'] = range(1, len(df) + 1)
    df['effective_date'] = datetime.today().strftime(constants.DATE_FORMAT)
    df['end_date'] = constants.future_date
    df['active_flag'] = True
    return df
