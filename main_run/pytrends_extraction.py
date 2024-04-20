import pandas as pd
import time
from serpapi import get_related_queries, str_to_bool

def too_many_request_error_loop(keyword):
    try:
        if keyword not in articles_keywords.keys(): 
            if is_it_test:
                related_queries = get_related_queries(keyword)
            else:
                related_queries = get_related_queries(keyword, date='2018-01-01 2023-12-31',use_api_key=use_api_key)
            
            if related_queries is not None:
                top = related_queries['top']  
                query = [item['query'] for item in top]
                score = [item['extracted_value'] for item in top]
                row_top_queries.append(query) 
                row_top_score.append(score)
                articles_keywords[keyword] = [query,score]
            else:
                print('None for {}'.format(keyword))
                row_top_queries.append([""])
                row_top_score.append([-1])
                articles_keywords[keyword] = [[""],[-1]]
            time.sleep(1)
        else: 
            row_top_queries.append(articles_keywords[keyword][0])
            row_top_score.append(articles_keywords[keyword][1])
    except Exception as err:
        print(err)
        return True
    return False

# ------------------------------------------------------------------------------------------------------------------------------------------------------------

file_path_keywords = 'dataset_klucove_slova.csv' 
df_keywords = pd.read_csv(file_path_keywords, sep=';', encoding='utf-8')
file_path_top = 'data_related{}.csv'.format(time.time()) 
df_top = pd.DataFrame(columns=['OBSAH', 'ODKAZ', 'KLUCOVE SLOVO','TOP'])
use_api_key= str_to_bool(input("Do you want to use api key? y/n"))
is_it_test = str_to_bool(input("Is it test only? y/n"))


articles_keywords = {}
top_queries = []

for index, row in df_keywords.iterrows(): 
    if pd.notna(row['KLUCOVE SLOVO']): 
        value = row['KLUCOVE SLOVO'] 
        row_top_queries = []  
        row_top_score = []
        row_top_queries_score = []
        print(index)
        keyword = value.strip() 
        while(too_many_request_error_loop(keyword)):
                time.sleep(60)
                print("It's waiting")
        
        for index1, items in enumerate(row_top_queries): 
            for index2, item in enumerate(items): 
                temp_df = pd.DataFrame({'OBSAH': [row['OBSAH']], 'ODKAZ': [row['ODKAZ']], 'KLUCOVE SLOVO': [keyword], 'TOP': [item], 'SKORE': [row_top_score[index1][index2]]})
                df_top = pd.concat([df_top, temp_df], ignore_index=True)
                df_top.to_csv(file_path_top, sep=';', encoding='utf8', index=False)
    else:
            
            temp_df = pd.DataFrame({'OBSAH': [row['OBSAH']], 'ODKAZ': [row['ODKAZ']], 'KLUCOVE SLOVO': [keyword], 'TOP': [''], 'SKORE': [0] })
            df_top = pd.concat([df_top, temp_df], ignore_index=True)
            df_top.to_csv(file_path_top, sep=';', encoding='utf8', index=False)


