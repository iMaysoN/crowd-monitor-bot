import requests
import json
import re
from datetime import datetime
import time


link = "https://crowdrepublic.ru/x/project/1014958?mode=normal&scenario%5B%5D=finance&scenario%5B%5D=basic"
headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }
r = requests.get(link, headers = headers)
print(r.text)
result = re.match("<textarea>(.*)</textarea>", r.text)
text = result.group(1)
json_string = json.loads(text)

title = json_string["Project"]["title"]
goals_completed = json_string["Project"]["count"]["goals_completed"]
ts = json_string["Project"]["time_chance"]
print(datetime.utcfromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S'))

print(text)
print(json_string["Project"])