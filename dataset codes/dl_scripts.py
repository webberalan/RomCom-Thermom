#overall notes:
# each URL is in the dictonary
# it looks like this:  https://imsdb.com/genre/Romance/Movie Scripts/10 Things I Hate About You Script.html
# the URL to the script looks like this: https://imsdb.com/genre/Romance/Movie Scripts/10-Things-I-Hate-About-You-Script.html
# so the base url changed to /scripts/ and it replaced the spaces and punctuation (among other things) with a hyphen

import json
import requests
from bs4 import BeautifulSoup


#open the deduped json file
with open('deduped.json', 'r') as new:
    data = json.load(new)

#loop through each data dictonary
    for movie in data:
        movie['screenplay_text'] = []
        url = movie['a_url']
#split off the last piece of the URL
        end_url = url.split('/')[-1].replace(' ', '-').replace('-Script', '').replace(':', '')
#build a new URL with the base 'https://imsdb.com/scripts/'
        new_url = 'https://imsdb.com/scripts/' + end_url

#use requests to download the HTML page
#parse with Beautiful Soup and pull out just script text
#add the script text to a **new key** in the dictonary
#save out the json files

        r = requests.get(new_url)
        soup = BeautifulSoup(r.text,features='html.parser')
        script = soup.find('pre')

        if script == None:
            print("This one is off!", new_url)
            continue

        for b in script.find_all(text=True):

            text = str(b).strip()
            #b.text.strip()
            if text=="":
                continue
            if "<b>" in text:
                continue

            movie['screenplay_text'].append(text)

        with open('screenplay.json', 'w') as new:

            json.dump(data, new, indent=2)
