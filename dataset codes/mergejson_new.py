import json

# make a place to hold the data
# the key will be the URL since it is unique (can hold multiple scrap data sets and ignore duplicates)

all_data = {}

#make a list of the files

files = ['imsdb_comedy_data.json', 'imsdb_romance_data.json']

for file in files:

#open load

	with open(file) as infile:

		jsondata = json.load(infile)

		#loop through all the titles

		for title_dictonary in jsondata:

			url = title_dictonary['a_url']

			#don't take the whole url, just take the last piece of it, the title of the movie
			# split the URL in to a list, seperating the string on every occrance of a '/' char

			url_pieces = url.split('/')

			# take the last item of list, which will be the title + the .html

			movie_title = url_pieces[-1]

			# add it to all_data, if it is already there it will simply overwrite it/dedupe it in the process

			all_data[movie_title] = title_dictonary


deduped_list = []

#now loop through the keys, which the values are the dictonary, add them to the list

for key in all_data:

	deduped_list.append(all_data[key])

import operator

#other method:  deduped_list.sort(key=operator.itemgetter('title'))
deduped_list = sorted(deduped_list, key=lambda k: k['title'])

with open('deduped.json','w') as out:
	json.dump(deduped_list,out,indent=2)
