import requests
from functools import lru_cache

@lru_cache(maxsize=1)
def get_all_countries():
    url = "https://restcountries.com/v3.1/all"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    return [country["name"]["common"] for country in data]
