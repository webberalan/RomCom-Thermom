#open Google Cloud NL module downloaded via pip3
from google.cloud import language
import json

#before you run this you need to download your .json file key from Google Cloud NL (need account)
#instructions via https://www.freecodecamp.org/news/how-to-make-your-own-sentiment-analyzer-using-python-and-googles-natural-language-api-9e91e1c493e/
#once you have the json key file you need to set it in the Terminal
#export GOOGLE_APPLICATION_CREDENTIALS=path/to/the/json.key

#this is the function that talks to the API, it returns a dictonary with the text, score and magnitude
def analyze_text_sentiment(text):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)

    response = client.analyze_sentiment(document=document)

    sentiment = response.document_sentiment
    results = {
        'text':text,
        'score':sentiment.score,
        'magnitude': sentiment.magnitude
    }

    return results

#here is where you use a function to break the screenplay text into 'chunks'
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

#open the json screenplay database file you want to run sentiment analysis on
#change for different movies
with open('ItHappenedOneNight.json', 'r') as database:
    data = json.load(database)

for screen_play in data:
    screen_play_text =  screen_play['screenplay_text']

#clean the text
    all_text_lines_clean = []
    for text_line in screen_play_text:
        text_line = " ".join(text_line.split())
        if text_line.upper() == text_line:
            continue
        all_text_lines_clean.append(text_line)

#make a new place to store all the results
#you can change the amount of lines you want in the chunk per the number below
    clean_chunks = chunks(all_text_lines_clean, 175)
    clean_chunks = list(clean_chunks)
    screen_play['line_results'] = []
    counter = 0
    for line in clean_chunks:
        line = " ".join(line)

#send it to the API
        api_results = analyze_text_sentiment(line)

        print(api_results)

        screen_play['line_results'].append(api_results)

        counter+=1

        print('on line ', counter, 'of', len(all_text_lines_clean))

#designate new file name +"_with_score.json" for new results dictionary
    with open('ItHappenedOneNight_with_score.json', 'w') as out:
        json.dump(data, out, indent=2)

    #only do one title per file (if more than one), remove this to keep going
    break
