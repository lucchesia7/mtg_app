import pickle
from classes.scryfall_classes import Data_Handling
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import make_pipeline
from pathlib import Path

# Set folder directory to store data
# C: set to lowercase. Fixed with .upper and str concat
folder_dir = f'{Path(__file__).parents[0]}\\data'
folder_dir = folder_dir[0].upper() + folder_dir[1:]

# # Instantiate DataFrame Object
df = Data_Handling().cleaning_scryfall_data()
print('DataFrame Object has been created')

# # Separate the DataFrame into tokens and cards
df_tokens = df[df['type_line'].str.contains(
    'Card // Card|Token|Scheme|Vanguard|Emblem|Card|Plane', regex=True)]
df_cards = df[~df['type_line'].str.contains(
    'Card // Card|Token|Scheme|Vanguard|Emblem|Card|Plane', regex=True)]
print('Data Separation has been completed')

# # Create Lemmatization of card descriptions
df_cards['lemmas'] = Data_Handling().lemma(df_cards)
print('Lemmas have been created')

# # Save DataFrames to CSV file
# df_cards.to_csv(f'{folder_dir}\\oracle_data.csv')
# df_tokens.to_csv(f'{folder_dir}\\token_data.csv')
# print("DataFrame's have been saved to their files")

# Create vectorizer and save vocabulary to file
# vect = TfidfVectorizer()

# vect.fit(df_cards['lemmas'])
# vect_vocab = vect.vocabulary_
# pickle.dump(vect, open(f'{folder_dir}\\vect.pk', 'wb'))
# print('Created vectorizer vocabulary')

# # Create model and save to file
# model = NearestNeighbors(n_neighbors=13)
# model.fit(vect.transform(df_cards['lemmas']))
# pickle.dump(model, open(f'{folder_dir}\\model.pk', 'wb'))
# print('Model has been created and saved')
# print('Completed all required updates')


#### UPDATE ####
# Create pipeline object
pipe = make_pipeline(
    TfidfVectorizer(),
    NearestNeighbors(n_neighbors=13)
)
pipe.fit(df_cards['lemmas'].astype(str))
pickle.dump(pipe, open(f'{folder_dir}\\pipe.pk', 'wb'))

print('Created Pipeline and saved to file')