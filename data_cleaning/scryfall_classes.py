import numpy as np
import pandas as pd
import re
import warnings
warnings.filterwarnings("ignore")
import requests

class Data_Scraping:
    def __init__(self):
        return
    def create_data_frame(self):
        response = requests.get('https://api.scryfall.com/bulk-data')
        j = response.json()
        df = pd.DataFrame(j['data'])
        return df
    
    def scrape_oracle_uri(self):
        df = self.create_data_frame()
        self.filepath = df['download_uri'][df['type'] == 'oracle_cards'][0]
        return self.filepath
    
    def scrape_default_uri(self):
        df = self.create_data_frame()
        self.filepath = df['uri'][df['type'] == 'default_cards'][0]
        return self.filepath
    
    def get_all_cards(self):
        df = self.create_data_frame()
        self.filepath = df['uri'][df['type'] == 'all_cards'][0]
        return self.filepath
    def get_artwork(self):
        df = self.create_data_frame()
        self.filepath = df['uri'][df['type'] == 'unique_artwork'][0]
        return self.filepath
    
class Data_Handling(Data_Scraping):
    def __init__(self):
        super().__init__()

    def wrangle_oracle_uri(self):
        super().scrape_oracle_uri()
        return self.filepath
    
    def cleaning_scryfall_data(self):
        #Fix NA Values for edhrec_rank
        self.wrangle_oracle_uri()
        self.df = pd.read_json(self.filepath)
            
        if 'edhrec_rank' in self.df.columns:
            edh_fix = self.df[self.df['edhrec_rank'].isna() == True]
            counter = 22665 # Max rank + 1
    
            edh_fix.edhrec_rank = range(counter, (counter + len(edh_fix)))
            self.df.loc[edh_fix.index, :] = edh_fix[:]
            self.df['edhrec_rank'] = self.df['edhrec_rank'].astype('int64')
    
        # Fix power column
        if 'power' in self.df.columns:
            self.df['power'].loc[self.df['power'].isna() == True] = 0
        
        # Fix Toughness Columns
        if 'toughness' in self.df.columns:
            self.df['toughness'].loc[self.df['toughness'].isna() == True] = 0
            
        # Fix CMC Column
        if 'cmc' in self.df.columns:
            self.df['cmc'].loc[17411] = 1
            self.df['cmc'] = self.df['cmc'].astype('int64')
        
        if 'oracle_id' in self.df.columns:
            self.df.set_index('oracle_id', inplace=True)
        
        if 'colors' in self.df.columns:
            self.df['colors'] = self.df['colors'].str[0]
            self.df['colors'].fillna('C', inplace=True)

        if 'color_identity' in self.df.columns:
            self.df['color_identity'] = self.df['color_identity'].str[0]
            self.df['color_identity'].fillna('C', inplace=True)
            
        if 'keywords' in self.df.columns:
            self.df['keywords'] = self.df['keywords'].str[0]
            self.df['keywords'].fillna('None', inplace =True)
        
        if 'mana_cost' in self.df.columns:
            self.df['mana_cost'].fillna(self.df['cmc'].astype(str), inplace=True)
           
            l = []
            for val in self.df.mana_cost:
                val = re.sub(r'[{]', '', str(val))
                val = re.sub(r'[}]', '/', val)
                val = val.strip('/')
                l.append(val)
            self.df['mana_cost'] = l
            self.df['mana_cost'] = np.where(self.df['mana_cost'] == '', self.df['cmc'], self.df['mana_cost'])
        

            
        return self.df
    
    def modeling_prep_mtg_oracle(self, df):
        # Drop columns for modeling purposes
        drop_cols = ['id', 'multiverse_ids', 'tcgplayer_id', 'cardmarket_id', 'lang', 'object', 
                     'released_at', 'uri', 'scryfall_uri', 'layout', 'highres_image', 'image_status', 
                     'image_uris', 'games', 'frame', 'full_art', 'textless', 'booster', 'story_spotlight', 'prices',
                     'legalities', 'reserved', 'foil', 'nonfoil', 'card_back_id', 'artist', 'artist_ids', 'illustration_id', 
                     'border_color', 'oversized', 'finishes', 'scryfall_set_uri', 'rulings_uri', 'promo', 'set', 'set_uri', 'set_search_uri', 
                     'reprint', 'variation', 'set_id', 'prints_search_uri', 'collector_number', 'digital', 'mtgo_id']
        
        if 'oracle_text' in df.columns:
            df['oracle_text'].dropna(inplace=True)
            
        if 'related_uris' in df.columns:
            target_cards = df['related_uris']
            drop_cols.append('related_uris')
        
        if 'type_line' in df.columns:
            a = df[df['type_line'].str.contains('Token Creature')]
            df.drop(labels=a.index, inplace=True)
                
        if 'set_name' in df.columns:
            c = df[df['set_name'].str.contains('Art Series')]
            df.drop(labels = c.index, inplace=True)
        df.drop(index = df[df['name'] == 'Gleemax'].index,inplace=True)
            
        drop_cols_high_nan = [col for col in df.columns if (df[col].isna().sum() / len(self.df) *100) > 35]
        for col in drop_cols_high_nan:
            drop_cols.append(col)
        df.drop(columns = drop_cols, inplace=True)

        return df, target_cards
    
if __name__ == '__main__':
    ds = Data_Handling()
    df = ds.cleaning_scryfall_data()
    df,target = ds.modeling_prep_mtg_oracle(df)
    print(df)
    print('done')