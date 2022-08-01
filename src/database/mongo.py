import pymongo
from classes.scryfall_classes import Data_Handling
DBNAME = 'test'
PASSWORD = 'admin'

client = pymongo.MongoClient(f'mongodb+srv://server:{PASSWORD}@test.xjeu0.mongodb.net/{DBNAME}?retryWrites=true&w=majority')

dh = Data_Handling()
df = dh.cleaning_scryfall_data()
df, targ = dh.modeling_prep_mtg_oracle(df)

db = client.test
c = db.test

for index in df.index:
    c.insert_one({
        'id' : index,
        'Name' : df['name'][index],
        'Description': df['oracle_text'][index],
        'Type': df['type_line'][index],
        'Colors' : df['colors'][index],
        'Color Identity' : df['color_identity'][index],
        'Rarity' : df['rarity'][index],
        'Set': df['set_name'][index],
        'Power': df['power'][index],
        'toughness': df['toughness'][index],
        'EDH Recommendation Rank': int(df['edhrec_rank'][index])
    })

