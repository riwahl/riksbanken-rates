from fetch_data import fetch_data_for_series_for_range
import polars as pl

series = 'SEMB2YCACOMB'

data = fetch_data_for_series_for_range(series)

df = pl.DataFrame(data)

df.write_database(
    table_name = 'dev.polars_table',
    connection='postgresql://db_user:db_password@db:5432/db',
    engine='adbc'
)

