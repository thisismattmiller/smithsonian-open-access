import ujson
import re

# this just holds the over all record count
count = 0

# these hold all of the lookup counts we are going to be making
has_media_loopup = {}
has_no_media_loopup = {}
freetext_fields = {}
indexedStructured_fields = {}
date_index = {}
topic_index = {}
topic_index_by_dept = {}
country_index = {}
width_height = {}

# these are the regular expression patterns to look for the mesurments in cm
cmx4 = re.compile(r"([0-9]+\.*[0-9]*)\s+c*m*[×x ]*\s([0-9]+\.*[0-9]*)\s+c*m*[×x ]*([0-9]+\.*[0-9]*)\s+c*m*[×x ]*([0-9]+\.*[0-9]*)\s*cm")
cmx3 = re.compile(r"([0-9]+\.*[0-9]*)\s+c*m*[×x ]*([0-9]+\.*[0-9]*)\s+c*m*[×x ]*([0-9]+\.*[0-9]*)\s*cm")
cmx2 = re.compile(r"([0-9]+\.*[0-9]*)\s+c*m*[×x ]*([0-9]+\.*[0-9]*)\s*c*m")


with open('all_data.ndjson') as infile:

	# ope the big json file and loop through line by line
	for line in infile:

		# parse the line of json into data
		data = ujson.loads(line)	

		count+=1
		# every 100K records let us know where we are at
		if count % 100000 == 0:
			print(count)


		# the department is always there
		dept = data['content']['descriptiveNonRepeating']['data_source']

		# look through each date field and add it to the lookup count
		if 'indexedStructured' in data['content']:
			if 'date' in data['content']['indexedStructured']:
				for date in data['content']['indexedStructured']['date']:
					if date not in date_index:
						date_index[date] = 0
					date_index[date]+=1

		# look through each topic field and add it to the lookup count
		if 'indexedStructured' in data['content']:
			if 'topic' in data['content']['indexedStructured']:
				for topic in data['content']['indexedStructured']['topic']:
					if topic not in topic_index:
						topic_index[topic] = 0
					topic_index[topic]+=1

					if dept not in topic_index_by_dept:
						topic_index_by_dept[dept] = {}

					if topic not in topic_index_by_dept[dept]:
						topic_index_by_dept[dept][topic] = 0

					topic_index_by_dept[dept][topic]+=1



		# look through each geoLocation field and add it to the lookup count
		if 'indexedStructured' in data['content']:
			if 'geoLocation' in data['content']['indexedStructured']:
				for x in data['content']['indexedStructured']['geoLocation']:
					if 'L2' in x:
						if isinstance(x['L2'], str):
							k =x['L2']
						else:
							k = x['L2']['content']

						if k not in country_index:
							country_index[k] = 0

						country_index[k]+=1

		# look through each physicalDescription field see if it has the string "cm" in it, if it does try our 3 reg ex patterns to try and pull out the height and width
		if 'freetext' in data['content']:
			if 'physicalDescription' in data['content']['freetext']:
				for x in data['content']['freetext']['physicalDescription']:
					if 'cm' in x['content']:

						height = None
						width = None

						s = cmx4.search(x['content'])
						if s:
							# print(s)
							# print(s.group(1), s.group(2),s.group(3),s.group(4))
							width = s.group(1)
							height = s.group(2)
						else:
							s = cmx3.search(x['content'])
							if s:
								# print(s)
								# print(s.group(1), s.group(2),s.group(3))
								width = s.group(1)
								height = s.group(2)

							else:
								s = cmx2.search(x['content'])
								if s:

									width = s.group(1)
									height = s.group(2)									
									# print(s)
									# print(s.group(1), s.group(2))
								# else:
								# 	print("SHHHHITTT")
								# 	print(x['content'])


						if width:
							wh_key = width + 'x' + height
							if wh_key not in width_height:
								width_height[wh_key] = {'count':0, 'hw': [width,height]}

							width_height[wh_key]['count']+=1




		
		# Build the basic, has media and field counts
		if 'online_media' in data['content']['descriptiveNonRepeating']:
			if data['content']['descriptiveNonRepeating']['data_source'] not in has_media_loopup:
				has_media_loopup[data['content']['descriptiveNonRepeating']['data_source']] = 0
			

			has_media_loopup[data['content']['descriptiveNonRepeating']['data_source']]+=1
		else:
			if data['content']['descriptiveNonRepeating']['data_source'] not in has_no_media_loopup:
				has_no_media_loopup[data['content']['descriptiveNonRepeating']['data_source']] = 0


			has_no_media_loopup[data['content']['descriptiveNonRepeating']['data_source']]+=1

		if 'freetext' in data['content']:
			for key in data['content']['freetext'].keys():
				if key not in freetext_fields:
					freetext_fields[key] = 0
				freetext_fields[key]+=1


		if 'indexedStructured' in data['content']:
			for key in data['content']['indexedStructured'].keys():
				if key not in indexedStructured_fields:
					indexedStructured_fields[key] = 0
				indexedStructured_fields[key]+=1


# write it out 
ujson.dump(has_media_loopup,open('stats/has_media_loopup.json','w'),indent=2)
ujson.dump(has_no_media_loopup,open('stats/has_no_media_loopup.json','w'),indent=2)
ujson.dump(indexedStructured_fields,open('stats/indexedStructured_fields.json','w'),indent=2)
ujson.dump(freetext_fields,open('stats/freetext_fields.json','w'),indent=2)
ujson.dump(width_height,open('stats/width_height.json','w'),indent=2)
ujson.dump(date_index,open('stats/date_index.json','w'),indent=2)
ujson.dump(topic_index,open('stats/topic_index.json','w'),indent=2)
ujson.dump(country_index,open('stats/country_index.json','w'),indent=2)
ujson.dump(topic_index_by_dept,open('stats/topic_index_by_dept.json','w'),indent=2)


