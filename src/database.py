from pathlib import Path
from dotenv import load_dotenv
from classes.scryfall_classes import Data_Handling
import pymongo
import pandas
import os


"""
Database file left for future use of user data. Currently, accessing local ram is faster than network speed. Will not store cards in DB.
"""
filepath = os.path.join(Path(__file__).parents[1], 'data\\.env')
load_dotenv(filepath)
mongo_url = os.getenv('mongo_url')
client = pymongo.MongoClient(mongo_url)
db = client.test
cards = db.cards


def upload():
    df = Data_Handling().cleaning_scryfall_data()
    df['lemmas'] = Data_Handling().lemma(df)
    df.reset_index(inplace=True)
    for x in range(len(df)):
        cards.insert_one(df.loc[x].to_dict())


def update():
    db.drop_collection('cards')
    cards = db.cards
    df = Data_Handling().cleaning_scryfall_data()
    df['lemmas'] = Data_Handling().lemma(df)
    df.reset_index(inplace=True)
    for x in range(len(df)):
        cards.insert_one(df.loc[x].to_dict())


def refresh():
    db.drop_collection('cards')
    db.create_collection('cards')


if __name__ == '__main__':
    refresh()
    upload()
    # print(filepath)
