import pandas as pd
from keybert import KeyBERT

file_path_preprocessed = 'dataset_predspracovany.csv' 
df_preprocessed = pd.read_csv(file_path_preprocessed, sep=';', encoding='utf-8')
file_path_keywords = 'dataset_klucove_slova.csv'
df_keywords = pd.DataFrame(columns=['OBSAH', 'ODKAZ', 'KLUCOVE SLOVO'])
 
kw_model = KeyBERT()

for index, row in df_preprocessed.iterrows():
        keywords = kw_model.extract_keywords(row['PREDSPRACOVANY'], keyphrase_ngram_range=(1, 2), stop_words=None)
        for i in range(3):
                keyword = keywords[i]
                temp_df = pd.DataFrame({'OBSAH': [row['OBSAH']], 'ODKAZ': [row['ODKAZ']], 'KLUCOVE SLOVO': [keyword[0]]})
                df_keywords = pd.concat([df_keywords, temp_df], ignore_index=True)
    
df_keywords.to_csv(file_path_keywords, sep=';', encoding='utf-8', index=False)




