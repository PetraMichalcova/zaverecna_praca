import pandas as pd
from pytrends.request import TrendReq
import time

def too_many_request_error_loop(keyword):
    try:
        if keyword not in articles_keywords.keys(): 
            pytrends.build_payload(kw_list=[keyword], timeframe='2018-01-01 2023-12-31', geo='') 
            related_queries = pytrends.related_queries()
            top = related_queries.get(keyword, {}).get('top', None)  
            if top is not None:
                query = top['query'].values
                row_top_queries.append(query) 
                articles_keywords[keyword] = query
            else:
                row_top_queries.append("")
                articles_keywords[keyword] = ""
            time.sleep(4)
        else: 
            row_top_queries.append(articles_keywords[keyword])
    except Exception as err:
        print(err)
        return True
    return False

# ------------------------------------------------------------------------------------------------------------------------------------------------------------

file_path_keywords = 'input_dataset_pytrends.csv' 
df_keywords = pd.read_csv(file_path_keywords, sep=';', encoding='utf8')
file_path_top = 'top_dataset_pytrends.csv'
df_top = pd.DataFrame(columns=['OBSAH', 'ODKAZ', 'KLUCOVE SLOVO','TOP'])

pytrends = TrendReq(hl='en-US', tz=360)

articles_keywords = {}
top_queries = []

for index, row in df_keywords.iterrows(): 
    if pd.notna(row['KLUCOVE SLOVO']): 
        value = row['KLUCOVE SLOVO'] 
        row_top_queries = []  
        row_top_queries_score = []
        print(index)
        keyword = value.strip() 
        while(too_many_request_error_loop(keyword)):
            time.sleep(60)
            print("It's waiting")
        
        for items in row_top_queries: 
            for item in items: 
                temp_df = pd.DataFrame({'OBSAH': [row['OBSAH']], 'ODKAZ': [row['ODKAZ']], 'KLUCOVE SLOVO': [keyword], 'TOP': [item]})
                df_top = pd.concat([df_top, temp_df], ignore_index=True)
                df_top.to_csv(file_path_top, sep=';', encoding='utf8', index=False)
    else:
        temp_df = pd.DataFrame({'OBSAH': [row['OBSAH']], 'ODKAZ': [row['ODKAZ']], 'KLUCOVE SLOVO': [keyword], 'TOP': [''] })
        df_top = pd.concat([df_top, temp_df], ignore_index=True)
        df_top.to_csv(file_path_top, sep=';', encoding='utf8', index=False)




