import requests
import pandas as pd
import warnings
warnings.filterwarnings("ignore")


class Data_Scraping:
    def __init__(self):
        self.df = None

        return

    def get_json_data(self, url='https://api.scryfall.com/bulk-data'):
        response = requests.get(url)
        j = response.json()
        self.df = pd.DataFrame(j['data'])
        return self.df

    def get_data_with(
            self,
            n='oracle_cards',
            url='https://api.scryfall.com/bulk-data'):
        self.get_json_data(url=url)
        filepath = self.df['download_uri'][self.df['type'] == n].reset_index(drop=True)[
            0]
        r = requests.get(filepath)
        self.return_frame = pd.DataFrame.from_dict(r.json())

        return self.return_frame
