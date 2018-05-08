import lxml.html
def parse_form(html):
	tree = lxml.html.fromstring(html)
	data = {}
	for e in tree.xpath(r'//input'):
		if e.get('name'):
			data[e.get('name')]=e.get('value')
	return data
