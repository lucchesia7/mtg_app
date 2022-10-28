import pandas as pd
import warnings
warnings.filterwarnings("ignore")
import requests

class Data_Scraping:
    def __init__(self):
        self.df = None
        
        return
    
    def get_json_data(self, url = 'https://api.scryfall.com/bulk-data'):
        response = requests.get(url)
        j = response.json()
        self.df = pd.DataFrame(j['data'])
        return self.df
    
    def get_data_with(self, n='oracle_cards', url = 'https://api.scryfall.com/bulk-data'):
        self.return_frame = None
        if type(self.df) == 'pandas.core.frame.DataFrame':
            filepath = self.df['uri'][self.df['type'] == n].reset_index(drop=True)[0]
            self.return_frame = pd.read_json(filepath)
            
        else:
            self.get_json_data(url = url)
            filepath = self.df['download_uri'][self.df['type'] == n].reset_index(drop=True)[0]
            self.return_frame = pd.read_json(filepath)
            
        return self.return_frame


if __name__ == '__main__':
    print(Data_Scraping().get_data_with())