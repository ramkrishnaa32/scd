from lib.helperFunctions import get_engine, read_table, enhance_customers_df, load_to_postgres_transactional
from lib import constants
import os

# postgres source table
engine = get_engine()
customers_t_df = read_table(engine, constants.source_table)

# applying enhancement
enhance_customers_df = enhance_customers_df(customers_t_df)

# loading to postgress
load_to_postgres_transactional(enhance_customers_df, constants.target_table, engine)