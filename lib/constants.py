DATE_FORMAT = "%Y-%m-%d"
future_date = "9999-12-31"
primary_key = ["customerid"]
slowly_changing_cols = [ "email","phone","address", "city", "state", "zipcode"]
implementation_cols = ["effective_date","end_date","active_flag"]

source_table = "customers_t"
target_table = "customers_scd"