import requests
from bs4 import BeautifulSoup
import json

all_items = []

url = f"https://imsdb.com/genre/Romance"
#f-string {replaces/abbreviates value}

r = requests.get(url)
soup = BeautifulSoup(r.text,features="html.parser")
#add html.parser to avoid warning message

script_p = soup.find_all("p")

for p in script_p:

    link = p.find('a')

    a_url = 'https://imsdb.com/genre/Romance' + link['href']

    script_title = p.find('a')

    title = script_title['title']

    Written_by = p.find('i')

    writers = Written_by.text
    #you'll want to use the .text to access the value of the element, not the element itself

    print(title)
    print(writers)
    print(a_url)

    all_items.append({
        'title' : title,
        'writers' : writers,
        'a_url' : a_url
    })

    print('______________')

    with open('imsdb_romance_data.json','w') as outfile:
        json.dump(all_items,outfile,indent=5)
