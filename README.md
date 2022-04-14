This project constitutes a Python-powered **_RomCom Thermom_**, made up of two main parts:

1)	a JSON dataset of 462 full-text romance and comedy screenplays, web scraped from IMSDb.com
2)	a sentiment analysis code, which utilizes Google’s machine learning-based Cloud Natural Language API

![alt text](https://raw.githubusercontent.com/webberalan/RomCom-Thermom/main/RomComThermomPhotoFinal.jpg?raw=true)

Inspiration for the _Thermom_ comes from my interest in storytelling structure, and draws upon the experiments of Kurt Vonnegut and Vladimir Propp in mapping out core types of narratives through shapes and irreducible units.  I came across several other programming projects playing off of Vonnegut and Propp’s ideas (Matthew Jockers’s [R syuzhet](https://blog.revolutionanalytics.com/2015/02/finding-the-dramatic-arc-of-novels-with-sentiment-analysis.html
), Dan Kuster’s [Jupyter notebook](https://indico.io/blog/plotlines/a-computer/490733/
) on Disney screenplays, and [story shape research](https://www.theatlantic.com/technology/archive/2016/07/the-six-main-arcs-in-storytelling-identified-by-a-computer/490733/
) at the University of Vermont and University of Adelaide), which were also influential.  Romantic comedies and the character tropes of reporter, tramp and heiress have been a particular node of personal investigation; the _RomCom Thermom_ provides a vehicle for further examination into the tone and emotional flow of characters’ interactions per this genre of narrative.  

While by no means exhaustive, the Internet Movie Script Database presents one of the most comprehensive, publically available collections of screenplays on the internet.  I chose IMSDb as the data source for the _Thermom_ due to its voluminous nature and for the sake of variety in content.  IMSDb also integrates information from the more famous IMDb into its records, which would make it easy to potentially link other movie elements to the dataset.  Screenplays on IMSDb are written in HTML and not accessible as PDFs, etc., making the JSON dataset of collected screenplays an even more pertinent and usable asset.  

**JSON Dataset**

I began forming the dataset by using the Beautiful Soup package to web scrape all movie titles that came up as results for the “Romance” genre.  This involved writing a Python script with a for loop to find and scrape all data as text from the ‘a’ section of the HTML paragraph for each “Romance” title, and the ‘i’ section for the names of the screenwriters.  This information, combined with the URL for each specific page, was parsed and written to a new JSON list of dictionaries, containing all of the basic “Romance” screenplay data.  I repeated the procedure with another Python script to obtain the results of the “Comedy” genre, creating a second JSON list of dictionaries with all of the basic “Comedy” screenplay data.  

Next, I concatenated the two datasets into one, using a for loop to dedupe all repeat entries, based off of the title key within individual JSON dictionaries.  I also added a lambda key command to return the cumulative results in alphabetical order by title.  The results were then dumped out to a new, single JSON dataset, containing all titles, writers and URLs of both “Romance” and “Comedy” genres.  

Since IMSDb’s actual screenplay content is located on a second page beyond each initial movie title and credits page, I had to employ another round of web scraping to capture the actual screenplay data as text.  Using the new, concatenated and deduped JSON file, I requested information from the second page of each screenplay by splitting off the end of the initial URL and formulating an equation for the second URL.  This was done by adding “scripts/” to the end of https://imsdb.com/ and then re-formulating the title of the movie with dashes instead of spaces or colons.  To bypass irregularities within particular HTML, I also wrote in several if statements, instructing Beautiful Soup to keep going to the next movie for continued screenplay extraction.  Screenplay data was culled from the ‘b’ element within the second URL for each movie, and then appended into a new ‘screenplay_text’ key within the concatenated JSON file, completing the dataset.  

As the final dataset is a large, 84 MB file, and quite extensive to scroll through (even when hiding individual ‘screenplay_text’ keys), I parsed and cleaned a simple version in OpenRefine, exporting only the titles, writers and URLs to a CSV file.  This file is intended to be used as a reference catalogue to call upon individual screenplays within the greater dataset.  

**Sentiment Analysis Code**

I researched a number of sentiment analysis techniques, both Lexicon and machine learning-based.  I found that while Lexicon-based packages like VADER seemed to be easy to incorporate into a Python script, they were mostly used within short, line-by-line context to analyze things like Tweets or song lyrics.  I tried machine learning-based APIs, Indico and Repustate, but found their websites had poor functionality and their customer service was unresponsive.  An associate pointed out the Google Cloud Natural Language API and, with some help, I was able to make an account and access a [JSON file key](https://www.freecodecamp.org/news/how-to-make-your-own-sentiment-analyzer-using-python-and-googles-natural-language-api-9e91e1c493e/).  

Going off of sample code on the Google CNL website, I formulated my own Python script.  This begins by importing the ‘language’ package from ‘google.cloud,’ and utilizes a function to talk to the machine learning-based API (‘def analyze_text_sentiment(text)’), asking it to return results for ‘text,’ ‘score’ and ‘magnitude.’  ‘Text’ is simply the portion of the screenplay being analyzed, ‘score’ is the ranking of happiness or sadness attributed to it, and ‘magnitude’ is the level of overall emotion contained within the text portion.  

The sentiment analysis code is customizable by modifying the JSON read and write filenames and the number of lines you would like to analyze within a segment.  While you could run sentiment analysis on the entire 462-screenplay database, it would take a painstakingly long time, thus you can make new, mini-JSON dictionaries for individual screenplays and use the filename within the ‘with open…’r’’ command, then dumping to a new ‘_with_score.json…’w’’ filename.  The current segment default is set to 175 lines (‘clean_chunks = chunks(all_text_lines_clean, 175’), which comes out to approximately 10 screenplay pages (which in turn averages 10 minutes of movie screen time), but this could be altered to a higher or lower number, or you could use docstrings on this portion of code to run line-by-line analysis through the entire screenplay.  

Before running the Python code, you need to set your JSON file key in the Terminal.  (This needs to be done for each new Terminal session utilizing the Google CNL API.)  Finally, you run the code, communicating with the machine learning-based API, which will append the JSON dictionaries you have sent and append them with the new key, ‘line_results,’ which contains each ‘text’ segment along with its corresponding positive, negative or neutral 'score,' and overall emotional ‘magnitude.’

**Conclusion**

For this project, I selected five classic romcoms to analyze:  _10 Things I Hate About You_, _Annie Hall_, _His Girl Friday_, _It Happened One Night_ and _The Apartment_.  Since the JSON database also contains results for movies which polarize towards the far ends of each of that hybrid’s corresponding genres, I also chose one movie that was obviously a comedy (_Beavis and Butt-Head Do America_) and one that was obviously a romance (_The Bodyguard_).  Detailed results with corresponding text are available at the GitHub link above, but I am also including the results for _10 Things I Hate About You_ below for quick reference:

  Pages 1-10:
"score": -0.10000000149011612,
"magnitude": 85.80000305175781
  Pages 11-20:
"score": -0.20000000298023224,
"magnitude": 75.5
  Pages 21-30:
"score": -0.10000000149011612,
"magnitude": 88.9000015258789
  Pages 31-40:
“score": 0.0,
"magnitude": 76.9000015258789
  Pages 41-50:
"score": -0.10000000149011612,
"magnitude": 66.80000305175781
  Pages 51-60:
"score": -0.10000000149011612,
“magnitude": 71.9000015258789
  Pages 61-70:
"score": -0.10000000149011612,
"magnitude": 77.4000015258789
  Pages 71-80:
"score": -0.10000000149011612,
"magnitude": 86.5999984741211
  Pages 81-90:
"score": -0.10000000149011612,
"magnitude": 82.0999984741211
  Pages 91-100:
"score": -0.10000000149011612,
"magnitude": 46.70000076293945

In the above screenplay and others, I found that the ‘score’ tends to not fluctuate very much, providing more of a monitored tone of the screenplay, whereas the ‘magnitude’ has its peaks and valleys, more in the tradition of Vonnegut’s story shape analysis.  I will be providing Tableau-generated visualizations of my selected examples in the near future, in addition to the detailed JSON files available on GitHub.

<div class='tableauPlaceholder' id='viz1649956493054' style='position: relative'><noscript><a href='#'><img alt='RomCom Thermom Dashboard ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ro&#47;RomComThermom&#47;RomComThermomDashboard&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='RomComThermom&#47;RomComThermomDashboard' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ro&#47;RomComThermom&#47;RomComThermomDashboard&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                

Overall, I believe the _RomCom Thermom_ can be useful as either a JSON dataset for someone to use however they want in examining one of the 462 screenplays available, or as a Python script to run sentiment analysis on various movie screenplays in various segments of text to take the temperature of anything from a Hugh Grant fluff vehicle to a Billy Wilder penned masterpiece.  


_Special thanks to Pratt Institute Professor Matt Miller and Erin Elsbernd for their assistance on the project_

Photo:  Cooper thermometer (physical scan by Alan Webber) and still from _It Happened One Night_ (1934) with Clark Gable and Claudette Colbert
