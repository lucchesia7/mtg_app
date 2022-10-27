from pathlib import Path
from dotenv import load_dotenv
from classes.scryfall_classes import Data_Handling
import pymongo
import pandas
import os

# filepath = os.path.join(Path(__file__).parents[1], 'classes\.env')
filepath = r'C:\Users\Alex Lucchesi\OneDrive\Documents\GitHub\MTG_app\src\classes\.env'
load_dotenv(filepath)
mongo_url = os.getenv('mongo_url')
client = pymongo.MongoClient(mongo_url)
db = client.test


def upload():
    df = Data_Handling().cleaning_scryfall_data()
    cards = db.cards
    for x in range(len(df)):
        cards.insert_one(df.loc[x].to_dict())

def update():
    df = Data_Handling().cleaning_scryfall_data()
    db.drop_collection('cards')
    cards = db.cards

def refresh():
    db.drop_collection('cards')
    db.create_collection('cards')

if __name__ == '__main__':
    # refresh()
    upload()
    print(filepath)