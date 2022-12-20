import json
import requests


url = 'https://api.dictionaryapi.dev/api/v2/entries/en/wyz'
response = requests.get(url).text
json_data =  json.loads(response)
#------------------------------------------------------can be random entry of subarray


#definition = json_data[0]["meanings"][0]['definitions'][0]['definition']

print(type(json_data))


