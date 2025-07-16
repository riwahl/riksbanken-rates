import psycopg2
from fetch_data import fetch_latest_data_for_series

series_ids = {
    'two_year_rate': 'SEMB2YCACOMB',
    'five_year_rate': 'SEMB5YCACOMB',
    'reference_rate': 'SECBREPOEFF'
}

def connect_to_db():
    print('Connecting to the PostgreSQL database...')
    try:
        conn = psycopg2.connect(
            host = 'localhost',
            port = 5000,
            dbname = 'db',
            user = 'db_user',
            password = 'db_password'
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        raise
        
def create_tables(conn: psycopg2.extensions.connection, series_ids: dict[str, any]) -> None:
    print('Creating table if it does not exist...')
    try:
        cursor = conn.cursor()
        for table_name, series_name in series_ids.items():
            cursor.execute(f"""
                CREATE SCHEMA IF NOT EXISTS dev;
                CREATE TABLE IF NOT EXISTS dev.{table_name} (
                    id SERIAL PRIMARY KEY,
                    date DATE NOT NULL,
                    value FLOAT NOT NULL,
                    series_id VARCHAR(50) NOT NULL,
                    inserted_at TIMESTAMP DEFAULT NOW()
                );
            """)
            conn.commit()
            print(f"Table dev.{table_name} created or already exists.")
    except psycopg2.Error as e:
        print(f"Error creating table: {e}")
        raise

def insert_records(conn, series_ids: dict[str, any], data_dict: dict[str, any]) -> None:
    try:
        cursor = conn.cursor()
        for table_name, series_name in series_ids.items():
            data = data_dict.get(table_name)
            cursor.execute(f"""
                INSERT INTO dev.{table_name} (
                    date,
                    value,
                    series_id,
                    inserted_at
                ) VALUES (%s, %s, %s, NOW())
                """, (
                    data['date'],
                    data['value'],
                    series_name,
                ))
            conn.commit()
            print(f"Record inserted into dev.{table_name} for date {data['date']}.")
    except psycopg2.Error as e:
        print(f"Error inserting records: {e}")
        raise

def main():
    try:
        data_dict = {series_name: fetch_latest_data_for_series(series_id) for series_name, series_id in series_ids.items()}
        conn = connect_to_db()
        create_tables(conn, series_ids)
        insert_records(conn, series_ids, data_dict)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()
            print("Database connection closed.")


  