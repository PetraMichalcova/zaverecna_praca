import pandas as pd
from pytrends.request import TrendReq
import time
from pytrends.exceptions import TooManyRequestsError

file_path_top = 'top_dataset_pytrends.csv'
df_top = pd.read_csv(file_path_top, sep=';', encoding='utf8')

file_path_score = 'score_dataset_pytrends.csv' 
df_score = pd.DataFrame(columns=['OBSAH', 'ODKAZ', 'KLUCOVE SLOVO','TOP','SKORE-18-19','SKORE-20-21','SKORE-22-23'])


def tooManyRequestError_loop(top):
    try:
        if top not in tops_for_score.keys():
            pytrends.build_payload(kw_list=[top], timeframe='2018-01-01 2019-12-31', geo='')
            interest_over_time = pytrends.interest_over_time()
            interest_values = interest_over_time[top]
            interest_score_year_1 = interest_values.mean()
            interest_over_time_list.append((top, interest_score_year_1))
                
            pytrends.build_payload(kw_list=[top], timeframe='2020-01-01 2021-12-31', geo='')
            interest_over_time = pytrends.interest_over_time()
            interest_values = interest_over_time[top]
            interest_score_year_2 = interest_values.mean()
            interest_over_time_list.append((top, interest_score_year_2))
                
            pytrends.build_payload(kw_list=[top], timeframe='2022-01-01 2023-12-31', geo='')
            interest_over_time = pytrends.interest_over_time()
            interest_values = interest_over_time[top]
            interest_score_year_3 = interest_values.mean()
            interest_over_time_list.append((top, interest_score_year_3))

            tops_for_score[top] = [interest_score_year_1, interest_score_year_2, interest_score_year_3]
            
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
        pytrends = TrendReq(hl='en-US', tz=360, timeout=(30, 30))
        value_top = row['TOP'] 
        interest_over_time_list = []
        top = value_top.strip() 
        print(index)
        tooManyRequestError_loop(top)
        time.sleep(1)

        temp_df = pd.DataFrame({'OBSAH': [row['OBSAH']], 'ODKAZ': [row['ODKAZ']], 'KLUCOVE SLOVO': [row['KLUCOVE SLOVO']], 'TOP': [row['TOP']], 'SKORE-18-19': [interest_over_time_list[0][1]], 'SKORE-20-21': [interest_over_time_list[1][1]], 'SKORE-22-23': [interest_over_time_list[2][1]]})
        df_score = pd.concat([df_score, temp_df], ignore_index=True)
        df_score.to_csv(file_path_score, sep=';', encoding='utf8', index=False)






