from pathlib import Path
from PIL import Image
from io import BytesIO
import requests
from models import Model
import pandas as pd
import ast
import os

filepath = os.path.join(Path(__file__).parents[1], 'data/oracle_data.csv')
class User_Functions():
    def __init__(self):
        self.df = pd.read_csv(filepath, low_memory=False)

    def img_return(self,card_name : str = 'Sol Ring'):
        """
        Input: Card name as a string. String set to autopopulate with Sol Ring. 
        Bug: Dual sided cards are not returning. Desired return would be both sides of the card, if not just the side requested.
        Would like to show 10 cards that have the same first few letters for users to choose from in a dropdown menu
        Output: Fully-detailed card image returned as output. 
        """
        s = self.df[self.df['name'].str.lower().str.startswith(str(card_name).lower())]['image_uris']
        for k in s:
            img_dic = ast.literal_eval(k)
        img_str = img_dic['normal']
        response = requests.get(img_str)
        img = Image.open(BytesIO(response.content))
        return img

    def card_lookup(self, card_name : str):
        """
        Input: Card name as a string. String set to autopopulate with Sol Ring.
        TODO: Return relevant card information. Then integrate into application with user search to return alongside the image.
        Output: All relevant details about the card available currently. 
        """
        #TODO
        # Provide all relevant card information. Return all to begin, then filter out what we don't want.
        pass

    def recommended_cards(self, card_name : str):
        """
        Input: Card name as str. Str set to autopopulate with Sol Ring.
        TODO: Create KNN model using description column within the dataframe. Use this model to output recommended cards to user.
        Desired output would be 10 related cards
        Output: 10 related cards to user input card name.
        """
        #TODO
        #Uses KNN model to create card recommendations
        model = Model()
        names = model.nn(card_name=card_name)
        return [self.img_return(name) for name in names[0][1:]]

if __name__ == '__main__':
    User_Functions()