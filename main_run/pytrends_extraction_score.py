import pandas as pd
import time
import statistics
from serpapi import get_interest_over_time, str_to_bool


file_path_top = 'dataset_top_reduced.csv'
df_top = pd.read_csv(file_path_top, sep=';', encoding='utf8')

file_path_score = 'interest_over_time{}.csv'.format(time.time()) 
df_score = pd.DataFrame(columns=['ODKAZ', 'KLUCOVE SLOVO','TOP','SKORE-18','SKORE-19','SKORE-20', 'SKORE-21','SKORE-22','SKORE-23'])

error_counter = 0
use_api_key= str_to_bool(input("Do you want to use api key? y/n"))
is_it_test = str_to_bool(input("Is it test only? y/n"))

def interest_mean(interests):
    values = [item['values'][0]['extracted_value'] for item in interests]
    return statistics.mean(values)

def processTop(top):
    try:
        if top not in tops_for_score.keys():
            if is_it_test:
                interest_over_time = get_interest_over_time(top)
                interest_score_year_1 = interest_mean(interest_over_time)
                interest_over_time_list.append((top, interest_score_year_1))
            else:
                interest_over_time = get_interest_over_time(top,timeframe='2018-01-01 2018-12-31',use_api_key=use_api_key) 
                interest_score_year_1 = interest_mean(interest_over_time)
                interest_over_time_list.append((top, interest_score_year_1))
                
            if is_it_test:
                interest_over_time = get_interest_over_time(top) 
                interest_score_year_2 = interest_mean(interest_over_time)
                interest_over_time_list.append((top, interest_score_year_2))
            else:
                interest_over_time = get_interest_over_time(top,timeframe='2019-01-01 2019-12-31',use_api_key=use_api_key) 
                interest_score_year_2 = interest_mean(interest_over_time)
                interest_over_time_list.append((top, interest_score_year_2))    
            if is_it_test:
                interest_over_time = get_interest_over_time(top) 
                interest_score_year_3 = interest_mean(interest_over_time)
                interest_over_time_list.append((top, interest_score_year_3))
            else:
                interest_over_time = get_interest_over_time(top,timeframe='2020-01-01 2020-12-31',use_api_key=use_api_key) 
                interest_score_year_3 = interest_mean(interest_over_time)
                interest_over_time_list.append((top, interest_score_year_3))

            if is_it_test:
                interest_over_time = get_interest_over_time(top) 
                interest_score_year_4 = interest_mean(interest_over_time)
                interest_over_time_list.append((top, interest_score_year_4))
            else:
                interest_over_time = get_interest_over_time(top,timeframe='2021-01-01 2021-12-31',use_api_key=use_api_key)
                interest_score_year_4 = interest_mean(interest_over_time)
                interest_over_time_list.append((top, interest_score_year_4))
                
            if is_it_test:
                interest_over_time = get_interest_over_time(top) 
                interest_score_year_5 = interest_mean(interest_over_time)
                interest_over_time_list.append((top, interest_score_year_5))
            else:
                interest_over_time = get_interest_over_time(top,timeframe='2022-01-01 2022-12-31',use_api_key=use_api_key) 
                interest_score_year_5 = interest_mean(interest_over_time)
                interest_over_time_list.append((top, interest_score_year_5))    
            if is_it_test:
                interest_over_time = get_interest_over_time(top)
                interest_score_year_6 = interest_mean(interest_over_time)
                interest_over_time_list.append((top, interest_score_year_6))
            else:
                interest_over_time = get_interest_over_time(top,timeframe='2023-01-01 2023-12-31',use_api_key=use_api_key) 
                interest_score_year_6 = interest_mean(interest_over_time)
                interest_over_time_list.append((top, interest_score_year_6))

            tops_for_score[top] = [interest_score_year_1, interest_score_year_2, interest_score_year_3,
                                   interest_score_year_4, interest_score_year_5, interest_score_year_6]
            
        else:
            for score_for_year in tops_for_score[top]:
                interest_over_time_list.append((top, score_for_year))

    except Exception as err:
        print(err)
        return True
    return False


tops_for_score = {}

for index, row in df_top.iterrows(): 
    if pd.notna(row['TOP']): 
        value_top = row['TOP'] 
        interest_over_time_list = []
        top = value_top.strip() 
        print(index)
        processTop(top)

        try:
            temp_df = pd.DataFrame({'ODKAZ': [row['ODKAZ']], 'KLUCOVE SLOVO': [row['KLUCOVE SLOVO']], 'TOP': [row['TOP']], 'SKORE-18': [interest_over_time_list[0][1]], 'SKORE-19': [interest_over_time_list[1][1]], 'SKORE-20': [interest_over_time_list[2][1]], 'SKORE-21': [interest_over_time_list[3][1]], 'SKORE-22': [interest_over_time_list[4][1]], 'SKORE-23': [interest_over_time_list[5][1]]})
            df_score = pd.concat([df_score, temp_df], ignore_index=True)
            df_score.to_csv(file_path_score, sep=';', encoding='utf8', index=False)
        except IndexError as e:
            print(str(e))






