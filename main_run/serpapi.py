import requests
import json

api_key = None

def load_api_key():
    global api_key
    if api_key is not None:
        return api_key
    file_path = "apikey.txt"
    try:
        with open(file_path, "r") as file:
            api_key = file.read()
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    return api_key

def str_to_bool(s):
    s = s.lower()
    if s in {"yes", "y", "true"}:
        return True
    elif s in {"no", "n", "false"}:
        return False
    else:
        raise ValueError("Invalid input, cannot convert to boolean")

def text_to_json(text):
    try:
        json_data = json.loads(text)
        return json_data
    except json.JSONDecodeError as e:
        print(f"Error: {e}")
        return None

def get_web_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Error: Failed to retrieve content from {url}. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def get_related_queries(query, date=None, use_api_key=False):
    url = "https://serpapi.com/search.json?engine=google_trends&q={}&data_type=RELATED_QUERIES".format(query)
    if date is not None:
        url += '&date={}'.format(date) 
    if use_api_key:
        url += '&api_key={}'.format(load_api_key())
    content = get_web_content(url)
    if content:
        content_dict = text_to_json(content)
        if 'related_queries' in content_dict:
            return content_dict['related_queries']
    return None

def get_interest_over_time(query, timeframe=None, use_api_key=False):
    url = "https://serpapi.com/search.json?engine=google_trends&q={}&data_type=TIMESERIES".format(query)
    if timeframe is not None:
        url += '&date={}'.format(timeframe) 
    if use_api_key:
        url += '&api_key={}'.format(load_api_key())
    content = get_web_content(url)
    if content:
        return text_to_json(content)['interest_over_time']['timeline_data']
    return None

# Example usage

#tst = get_related_queries('coffee')
#print(tst)