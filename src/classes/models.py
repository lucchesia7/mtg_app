from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import spacy

class Model():
    def __init__(self):
        self.df = pd.read_csv(r'C:\Users\Alex Lucchesi\OneDrive\Documents\GitHub\MTG_app\src\classes\oracle_data.csv', 
                              low_memory=False)
        def dummy_func(doc):
            return doc
        self.vect = TfidfVectorizer(tokenizer = dummy_func,
                                   preprocessor= dummy_func,
                                   token_pattern=None)
        self.vect.fit(self.df['lemmas'])
        dtm = self.vect.transform(self.df['lemmas'])

        self.nnm = NearestNeighbors(n_neighbors=10, algorithm='auto')
        self.nnm.fit(dtm)


    

    def nn(self, card_name:str):
        names = []
        doc = self.vect.transform([self.df['lemmas'][self.df['name'] == card_name]])
        n_index = self.nnm.kneighbors(doc, n_neighbors=10, return_distance=False)

        for index in n_index:
            names.append(self.df['name'][index].values)
        return names
    
if __name__ == '__main__':
    cl = Model()
    names = cl.nn('Static Orb')
    for name in names[0]:
        print(name)