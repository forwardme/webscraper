import urllib2
import json
import string
template_url = "http://example.webscraping.com/places/ajax/search.json?&search_term={}&page_size=10&page={}"
countries = set()

for letter in string.lowercase:
	page = 0
	while True:
		html = urllib2.urlopen(template_url.format(letter,page)).read()
		try:
			ajax = json.loads(html)
		except ValueError as e:
			print e
			ajax = None
		else:
			for record in ajax['records']:
				countries.add(record['country'])
		page += 1
		if ajax is None or page >= ajax['num_pages']:
			break

print countries