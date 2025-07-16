import requests 
import pandas as pd
from datetime import date, timedelta, datetime


current_date = date.today().strftime('%Y-%m-%d')
yesterdays_date = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d') # Data for yesterday is made available on 9 A.M. CET today

series_ids = {
    'two_year': 'SEMB2YCACOMB',
    'five_year': 'SEMB5YCACOMB',
    'reference_rate': 'SECBREPOEFF'
}

BASE_URL = 'https://api.riksbank.se/swea/v1/Observations'
BASE_URL_INTERVAL = 'https://api.riksbank.se/swea/v1/Observations' #/{seriesId}/{from}/{to}'
BASE_URL_LATEST = 'https://api.riksbank.se/swea/v1/Observations/Latest'#/{seriesId}' 

def fetch_latest_data_for_series(series_id: str) -> dict[str, any]:
    """
    Takes a series ID and fetches the data for yesterday's date.
    The data is fetched from the Riksbank API and returned as a JSON object.
    """
    api_url = f'{BASE_URL_LATEST}/{series_id}'
    print(api_url)
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        print(f"Data for {series_id} on {response.json()['date']} fetched successfully.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        raise

# if __name__ == "__main__":
#     # Example usage
#     try:
#         data = fetch_latest_data_for_series(series_ids['two_year'])
#         print(data)
#     except Exception as e:
#         print(f"Failed to fetch data: {e}")

# print(fetch_latest_data_for_series(series_ids['two_year']))
# responses = {key: requests.get(f'{BASE_URL}/{value}/{yesterdays_date}') for key, value in series_ids.items()}

# two_year_data = pd.json_normalize(responses['two_year'].json())
# five_year_data = pd.json_normalize(responses['five_year'].json())
# reference_rate_data = pd.json_normalize(responses['reference_rate'].json())
