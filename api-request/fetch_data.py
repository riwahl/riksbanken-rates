import requests
from datetime import date

BASE_URL_INTERVAL = (
    "https://api.riksbank.se/swea/v1/Observations"  # /{seriesId}/{from}/{to}'
)
BASE_URL_LATEST = "https://api.riksbank.se/swea/v1/Observations/Latest"  # /{seriesId}'


def fetch_latest_data_for_series(series_id: str) -> dict[str, any] | None:
    api_url = f"{BASE_URL_LATEST}/{series_id}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        print(
            f"Data for {series_id} on {response.json()['date']} fetched successfully."
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        raise


def fetch_data_for_series_for_range(
    series_id: str, start_date: str = '2024-01-01', end_date: str = str(date.today())
) -> dict[str, any] | None:
    api_url = f"{BASE_URL_INTERVAL}/{series_id}/{start_date}/{end_date}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        latest_available_date = data[-1]["date"]
        if latest_available_date < end_date:
            print(
                f"NOTE: Data for {series_id} is only available up to {latest_available_date}, not {end_date}."
            )
        print(
            f"Data for {series_id} from {start_date} to {latest_available_date if latest_available_date < end_date else end_date} fetched successfully."
        )
        return data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        raise