import pandas as pd
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
# pd.set_option("display.width", None)
# pd.set_option("display.max_colwidth", None) 
from datetime import date, datetime
from lib.helperFunctions import read_table, get_engine, load_to_postgres_transactional
from lib import constants

DATE_FORMAT = constants.DATE_FORMAT
future_date = constants.future_date
primary_key = ["customerid"]
scd_columns = ["email", "phone", "address", "city", "state", "zipcode"]
today = pd.to_datetime(datetime.today().date())
engine = get_engine()

# Target table
customers_scd_df = read_table(engine, constants.target_table)
df_active = customers_scd_df[customers_scd_df["active_flag"] == True]

# Source table
customers_t_df = read_table(engine, constants.source_table)

# Step 1: Join source with active target on primary key
df_joined = customers_t_df.merge(
    df_active,
    on=primary_key,
    how="left",
    suffixes=("_src", "_tgt")
)

# Step 2: Identify records to update (slowly changing fields changed)
condition = False
for col in scd_columns:
    condition |= df_joined[f"{col}_src"] != df_joined[f"{col}_tgt"]

df_updates = df_joined[condition]

# Step 3: Prepare records to expire in target
df_to_expire = customers_scd_df.merge(
    df_updates[primary_key],
    on=primary_key,
    how="inner"
).copy()
df_to_expire["end_date"] = today
df_to_expire["active_flag"] = False

# Step 4: Prepare new versions of updated records (with new SCD data)
cols_for_new_version = primary_key + [col + "_src" for col in customers_t_df.columns if col not in primary_key]
df_new_versions = df_updates[cols_for_new_version].copy()
df_new_versions.columns = customers_t_df.columns
df_new_versions["effective_date"] = today
df_new_versions["end_date"] = future_date
df_new_versions["active_flag"] = True

# Step 5: Identify new inserts (not in target)
df_inserts = customers_t_df.merge(
    df_active[primary_key],
    on=primary_key,
    how="left",
    indicator=True
).query('_merge == "left_only"').drop(columns="_merge")

df_inserts["effective_date"] = today
df_inserts["end_date"] = future_date
df_inserts["active_flag"] = True

# Step 6: Identify unchanged records (remain as-is)
df_unchanged = customers_scd_df[
    ~customers_scd_df[primary_key[0]].isin(df_to_expire[primary_key[0]])
]

# Step 7: Final result - union all
df_final = pd.concat([
    df_unchanged,
    df_to_expire,
    df_new_versions,
    df_inserts
], ignore_index=True)

df_final["effective_date"] = pd.to_datetime(df_final["effective_date"]).dt.strftime(DATE_FORMAT)
future_date_str = str(future_date)
df_final["end_date"] = df_final["end_date"].apply(
    lambda x: x if str(x) == future_date_str else pd.to_datetime(x).strftime(DATE_FORMAT)
)

print(df_final)

# loading to postgres
load_to_postgres_transactional(df_final, constants.target_table, engine)

