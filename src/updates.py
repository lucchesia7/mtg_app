import pickle
from classes.scryfall_classes import Data_Handling
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from pathlib import Path

# Set folder directory to store data
# C: set to lowercase. Fixed with .upper and str concat
folder_dir = f'{Path(__file__).parents[0]}\\data'
folder_dir = folder_dir[0].upper() + folder_dir[1:]
# Instantiate DataFrame Object
df = Data_Handling().cleaning_scryfall_data()

# Create Lemmatization of card descriptions
df['lemmas'] = Data_Handling().lemma(df)

# Separate the DataFrame into tokens and cards
df_tokens = df[df['type_line'].str.contains(
    'Card // Card|Token|Scheme|Vanguard|Emblem|Card|Plane', regex=True)]
df_cards = df[~df['type_line'].str.contains(
    'Card // Card|Token|Scheme|Vanguard|Emblem|Card|Plane', regex=True)]

# Save DataFrames to CSV file
df_cards.to_csv(f'{folder_dir}\\oracle_data.csv')
df_tokens.to_csv(f'{folder_dir}\\token_data.csv')

# Define function to return single doc


def dummy_fun(doc):
    return doc


# Create vectorizer and save vocabulary to file
vect = TfidfVectorizer(preprocessor=dummy_fun,
                       token_pattern=None,
                       tokenizer=dummy_fun)

vect.fit(df_cards['lemmas'])
vect_vocab = vect.get_feature_names()
pickle.dump(vect_vocab, open(f'{folder_dir}\\vectorizer_vocab', 'wb'))

# Create model and save to file
model = NearestNeighbors(n_neighbors=10)
model.fit(vect.transform(df['lemmas']))
pickle.dump(model, open(f'{folder_dir}\\model', 'wb'))
