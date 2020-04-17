import pandas as pd

import requests
import json

class Reader:
    def __init__(self, country=None):
        self.country = country
        if country is not None:
            self.read_covid19_data(country)

    def read_covid19_data(self, country):
        print(f"Reading data from 'https://api.covid19api.com' for country='{country}'")
        
        if self.country is None:
            self.country = country
        
        url = f"https://api.covid19api.com/dayone/country/{country}"
        payload = {}
        headers = {}

        resp = requests.request("GET", url, headers=headers, data=payload)

        self.data = json.loads(resp.text)
        assert isinstance(self.data, list), f"'{country}' is not a valid country"
    
        self.confirmed = []
        self.recovered = []
        self.deaths = []
        self.dates = []
        for x in self.data:
            self.confirmed.append(x['Confirmed'])
            self.recovered.append(x['Recovered'])
            self.deaths.append(x['Deaths'])
            self.dates.append(x['Date'].split('T')[0])
        
        self.df = pd.DataFrame({"Date": self.dates,
                                "Confirmed": self.confirmed,
                                "Recovered": self.recovered,
                                "Deaths": self.deaths}).groupby('Date').agg('sum')
        
    def get_confirmed(self):
        return self.df.Confirmed.values

    def get_recovered(self):
        return self.df.Recovered.values

    def get_deaths(self):
        return self.df.Deaths.values

    def get_dates(self):
        return self.df.index.values
