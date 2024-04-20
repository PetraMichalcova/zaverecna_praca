import pandas as pd

file_path_top = 'data_related1712998230.5670266.csv'
df_top = pd.read_csv(file_path_top, sep=';', encoding='utf8')

file_path_top_reduced = 'dataset_top_reduced.csv'
df_top_reduced = pd.DataFrame(columns=['ODKAZ', 'KLUCOVE SLOVO', 'TOP','ZDRAVIU PROSPESNY', 'RASTLINNE ZALOZENY'])

map_reduced = {}

for index, row in df_top.iterrows(): 
    link = row['ODKAZ']
    keyword = row['KLUCOVE SLOVO'] # rozdelenie hodnôt v riadku stĺpci 'Keywords'
    top = row['TOP']
    healty = row['ZDRAVIU PROSPESNY']
    plant = row['RASTLINNE ZALOZENY']
    link_keyword = link+keyword
    if(top == 'the' or top == 'what' or top == 'what is' or top == 'which' or top == 'in' or top == 'and' or top == 'how') or isinstance(top, float) or len(top.split(" ")) > 4:
        continue
    values = [link, keyword, top, healty, plant]
    
    if link_keyword not in map_reduced.keys():
        map_reduced[link_keyword] = [False]
        map_reduced[link_keyword].append(values)
    
    elif link_keyword in map_reduced.keys() and len(map_reduced[link_keyword]) < 4:
        map_reduced[link_keyword].append(values)
    
    elif len(map_reduced[link_keyword]) == 4 and map_reduced[link_keyword][0] == False:
        values = map_reduced[link_keyword]
        print("VALUES")
        print(values)
        for index,value in enumerate(values):
            if index==0:
                continue
            temp_df = pd.DataFrame({'ODKAZ': [value[0]], 'KLUCOVE SLOVO': [value[1]], 'TOP': [value[2]], 'ZDRAVIU PROSPESNY': [value[3]], 'RASTLINNE ZALOZENY': [value[4]]})
            df_top_reduced = pd.concat([df_top_reduced, temp_df], ignore_index=True)
        values[0] = True

df_top_reduced.to_csv(file_path_top_reduced, sep=';', encoding='utf8', index=False)
