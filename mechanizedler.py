import re
import urllib2
import urllib
import mechanize
import lxml.html
from lxml import etree
login_url = 'https://www.safaribooksonline.com/accounts/login/'
base_url='https://www.safaribooksonline.com/library/view/data-visualization-with/9781491920565/'

def createLinkList():
	link_list = []
	for i in range(21):
		link_list.append(base_url+'ch{:02}.html'.format(i+1))
	for i in range(5):
		link_list.append(base_url+'part{:02}.html'.format(i+1))
	link_list.append(base_url+'preface01.html')
	link_list.append(base_url+'preface02.html')
	link_list.append(base_url+'app01.html')
	return link_list

def login(login_url,browser):
	print 'login website...'
	browser.open(login_url)
	browser.select_form(nr=0)
	browser.form['email']='forwardme@163.com'
	browser.form['password1']='gaoyuan123'
	print 'submitting form:/n',browser.form
	response_html = browser.submit().get_data()
	tree = lxml.html.fromstring(response_html)
	if tree.xpath(r'//*[@id="login"]/header/h1'):
		print 'login failed.'
	else:
		print 'login successed.'

def gethtml(link_list,browser):
	figure_links = set()
	for link in link_list:
		print 'downloading link: ',link
		html = browser.open(link).get_data()
		tree = lxml.html.fromstring(html)
		figures = tree.xpath(r'//*[@id="sbo-rt-content"]//img')
		for fig in figures:
			figlink = fig.get('src')
			figname = figlink.split('/')[-1]
			figure_links.add("https://www.safaribooksonline.com"+figlink)
			html = re.sub(figlink,figname,html)
		with open(link.split('/')[-1],'wb') as file:
			file.write(html)
	return figure_links

def getfigure(figure_links):
	for figlink in figure_links:
		figname = figlink.split('/')[-1]
		print 'downloading fig : ',figname
		with open(figname,'wb') as file:
			file.write(urllib2.urlopen(figlink).read())


def run():
	br = mechanize.Browser()
	#br.set_all_readonly(False)    # allow everything to be written to
	br.set_handle_robots(False)   # ignore robots
	#br.set_handle_refresh(False)  # can sometimes hang without this
	br.addheaders =  [('User-agent','Firefox')]	      	# [('User-agent', 'Firefox')]
	login(login_url,br)
	getfigure(gethtml(createLinkList(),br))

if __name__ == "__main__":
	run()
