from lxml import html
import requests
import sqlite3
import bs4
from bs4 import BeautifulSoup as soup
import sqlite3
from urllib2 import urlopen as uReq
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def my_function():
	my_url = ['https://magicseaweed.com/Narragansett-Beach-Surf-Report/1103/', 
	'https://magicseaweed.com/2nd-Beach-Sachuest-Beach-Surf-Report/846/',
	'https://magicseaweed.com/Nahant-Surf-Report/1091/',
	'https://magicseaweed.com/Nantasket-Beach-Surf-Report/371/',
	'https://magicseaweed.com/Scituate-Surf-Report/372/',
	'https://magicseaweed.com/Cape-Cod-Surf-Report/373/',
	'https://magicseaweed.com/The-Wall-Surf-Report/369/',
	'https://magicseaweed.com/Green-Harbor-Surf-Report/864/',
	'https://magicseaweed.com/Cape-Ann-Surf-Report/370/',
	'https://magicseaweed.com/27th-Ave-North-Myrtle-Surf-Report/2152/',
	'https://magicseaweed.com/Cocoa-Beach-Surf-Report/350/']

	for url in my_url:

		page = requests.get(url)
		tree = html.fromstring(page.content)


		#This will create master list containing SwellSize, SwellInterval, & Airtemp
		intervals = tree.xpath('//*[@class="nomargin font-sans-serif heavy"]/text()')
		#Navigating through master list, breaking down 3 data categories into variables
		swellsizeft = intervals[0::5]
		swellintervalsec = intervals[2::5]
		airtempdegrees = intervals[4::5]

		# Next we will need to iterate through our per category lists, and add to DB!

		# ['A', 'B', 'C', 'D']
		# ['Swell Size', 'Junk', 'SwellInterval', 'Junk', 'Airtemp']
		# ['  2', '  ', '  11', '  ', '38', ]

		conn = sqlite3.connect('SurfSend.db')
		cursor = conn.cursor()
		cursor.execute('CREATE TABLE IF NOT EXISTS SurfReport(ID INTEGER PRIMARY KEY, SwellSizeFt TEXT, SwellIntervalSec TEXT, AirTemp TEXT )')

		for x, y, z in zip(swellsizeft, swellintervalsec, airtempdegrees):
				conn = sqlite3.connect('SurfSend.db')
				cursor = conn.cursor()
				# cursor.execute("INSERT INTO SurfReport VALUES (?,?,?)", (x,y,z))
				cursor.execute("INSERT INTO SurfReport (SwellSizeFt, SwellIntervalSec, AirTemp) VALUES (?,?,?)", (x,y,z,))
				conn.commit()
				cursor.close()
				conn.close()


def my_function2():
	#list of URLs to scrape from
	my_url = ['https://magicseaweed.com/Narragansett-Beach-Surf-Report/1103/', 
	'https://magicseaweed.com/2nd-Beach-Sachuest-Beach-Surf-Report/846/',
	'https://magicseaweed.com/Nahant-Surf-Report/1091/',
	'https://magicseaweed.com/Nantasket-Beach-Surf-Report/371/',
	'https://magicseaweed.com/Scituate-Surf-Report/372/',
	'https://magicseaweed.com/Cape-Cod-Surf-Report/373/',
	'https://magicseaweed.com/The-Wall-Surf-Report/369/',
	'https://magicseaweed.com/Green-Harbor-Surf-Report/864/',
	'https://magicseaweed.com/Cape-Ann-Surf-Report/370/',
	'https://magicseaweed.com/27th-Ave-North-Myrtle-Surf-Report/2152/',
	'https://magicseaweed.com/Cocoa-Beach-Surf-Report/350/']
	# opening up connecting, grabbing the page

	conn = sqlite3.connect('SurfSend.db')
	cursor = conn.cursor()
	cursor.execute('CREATE TABLE IF NOT EXISTS WindInfo(ID INTEGER PRIMARY KEY, WindMPH TEXT)')

	#iterate over list of URLS
	for url in my_url:
		#initiating python's ability to parse URL
		uClient = uReq(url)
	# this will offload our content in'to a variable
		page_html = uClient.read()
	# closes our client
		uClient.close()

	# html parsing
		#beautifulsoup magic
		page_soup = soup(page_html, "html.parser")
		#variable for soon to be parsed page
		wind = page_soup.findAll('td', class_=re.compile("text-center table-forecast-wind td-nowrap"))
		#prints the list of URLs we scraped from

	# iterates over parsed HTML
		for w in wind:
			#wavesize
			wi = w.find('span', class_='stacked-text text-right')
			winb = wi.text.strip()

			conn = sqlite3.connect('SurfSend.db')
			cursor = conn.cursor()
			# cursor.execute("INSERT INTO WindInfo VALUES (?)", (winb,))
			cursor.execute("INSERT INTO WindInfo (WindMPH) VALUES (?)", (winb,))
			conn.commit()
			cursor.close()
			conn.close()

def my_function3():
	my_url = ['https://magicseaweed.com/Narragansett-Beach-Surf-Report/1103/', 
	'https://magicseaweed.com/2nd-Beach-Sachuest-Beach-Surf-Report/846/',
	'https://magicseaweed.com/Nahant-Surf-Report/1091/',
	'https://magicseaweed.com/Nantasket-Beach-Surf-Report/371/',
	'https://magicseaweed.com/Scituate-Surf-Report/372/',
	'https://magicseaweed.com/Cape-Cod-Surf-Report/373/',
	'https://magicseaweed.com/The-Wall-Surf-Report/369/',
	'https://magicseaweed.com/Green-Harbor-Surf-Report/864/',
	'https://magicseaweed.com/Cape-Ann-Surf-Report/370/',
	'https://magicseaweed.com/27th-Ave-North-Myrtle-Surf-Report/2152/',
	'https://magicseaweed.com/Cocoa-Beach-Surf-Report/350/']

	for url in my_url:

		r = requests.get(url)

		html = r.text

		soup = BeautifulSoup(html, 'lxml')

		# wind_directions = soup.find_all('td', {"class":"text-center last msw-js-tooltip td-square background-success"})

		wind_dir = soup.find_all(class_=re.compile('^text-center last msw-js-tooltip td-square background-'))  

		conn = sqlite3.connect('SurfSend.db')
		cursor = conn.cursor()
		cursor.execute('CREATE TABLE IF NOT EXISTS WindDirection(ID INTEGER PRIMARY KEY, WindDescription TEXT)')

		for w in wind_dir:

			windd = w['title']
			print(w['title'])


			conn = sqlite3.connect('SurfSend.db')
			cursor = conn.cursor()
			# cursor.execute("INSERT INTO WindInfo VALUES (?)", (winb,))
			cursor.execute("INSERT INTO WindDirection (WindDescription) VALUES (?)", (windd,))
			conn.commit()
			cursor.close()
			conn.close()


def my_function4():

	url = 'https://magicseaweed.com/Narragansett-Beach-Surf-Report/1103/'

	conn = sqlite3.connect('SurfSend.db')
	cursor = conn.cursor()
	cursor.execute('CREATE TABLE IF NOT EXISTS IDGrab(ID INTEGER PRIMARY KEY, WindDescription TEXT)')

	r = requests.get(url)

	html = r.text

	soup = BeautifulSoup(html, 'lxml')

	# wind_directions = soup.find_all('td', {"class":"text-center last msw-js-tooltip td-square background-success"})

	wind_dir = soup.find_all(class_=re.compile('^text-center last msw-js-tooltip td-square background-'))  

	for w in wind_dir:

		windd = w['title']
		print(w['title'])


		conn = sqlite3.connect('SurfSend.db')
		cursor = conn.cursor()
		# cursor.execute("INSERT INTO WindInfo VALUES (?)", (winb,))
		cursor.execute("INSERT INTO IDGrab (WindDescription) VALUES (?)", (windd,))
		conn.commit()
		cursor.close()
		conn.close()


def my_function5():

	conn = sqlite3.connect('SurfSend.db')
	cursor = conn.cursor()
	cursor.execute("CREATE TABLE SurfMaster2 AS select SurfReport.ID, SurfReport.SwellSizeFt, SurfReport.SwellIntervalSec, WindInfo.WindMPH, WindDirection.WindDescription, SurfReport.AirTemp from SurfReport inner join WindInfo on SurfReport.ID = WindInfo.ID inner join WindDirection on WindInfo.ID = WindDirection.ID")
	cursor.execute("ALTER TABLE SurfMaster2 ADD beach_name TEXT")
	cursor.execute("UPDATE SurfMaster2 SET beach_name = 'Narragansett' WHERE ID BETWEEN 1 AND 56")
	cursor.execute("UPDATE SurfMaster2 SET beach_name = '2nd Beach' WHERE ID BETWEEN 57 AND 112;")
	cursor.execute("UPDATE SurfMaster2 SET beach_name = 'Nahant' WHERE ID BETWEEN 113 AND 168")
	cursor.execute("UPDATE SurfMaster2 SET beach_name = 'Nantasket' WHERE ID BETWEEN 169 AND 224")
	cursor.execute("UPDATE SurfMaster2 SET beach_name = 'Scituate' WHERE ID BETWEEN 225 AND 280")
	cursor.execute("UPDATE SurfMaster2 SET beach_name = 'Cape Cod' WHERE ID BETWEEN 281 AND 336")
	cursor.execute("UPDATE SurfMaster2 SET beach_name = 'NH Seacoast' WHERE ID BETWEEN 337 AND 392")
	cursor.execute("UPDATE SurfMaster2 SET beach_name = 'Green Harbor' WHERE ID BETWEEN 393 AND 448")
	cursor.execute("UPDATE SurfMaster2 SET beach_name = 'Cape Ann' WHERE ID BETWEEN 449 AND 504")
	cursor.execute("UPDATE SurfMaster2 SET beach_name = 'Myrtle Beach' WHERE ID BETWEEN 505 AND 560")
	cursor.execute("UPDATE SurfMaster2 SET beach_name = 'Cocoa Beach' WHERE ID BETWEEN 561 AND 616")
	cursor.execute("ALTER TABLE SurfMaster2 ADD Time_ID TEXT")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =1 WHERE id IN (1,57,113,169,225,281,337,393,449,505,561)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =2 WHERE id IN (2,58,114,170,226,282,338,394,450,506,562)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =3 WHERE id IN (3,59,115,171,227,283,339,395,451,507,563)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =4 WHERE id IN (4,60,116,172,228,284,340,396,452,508,564)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =5 WHERE id IN (5,61,117,173,229,285,341,397,453,509,565)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =6 WHERE id IN (6,62,118,174,230,286,342,398,454,510,566)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =7 WHERE id IN (7,63,119,175,231,287,343,399,455,511,567)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =8 WHERE id IN (8,64,120,176,232,288,344,400,456,512,568)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =9 WHERE id IN (9,65,121,177,233,289,345,401,457,513,569)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =10 WHERE id IN (10,66,122,178,234,290,346,402,458,514,570)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =11 WHERE id IN (11,67,123,179,235,291,347,403,459,515,571)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =12 WHERE id IN (12,68,124,180,236,292,348,404,460,516,572)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =13 WHERE id IN (13,69,125,181,237,293,349,405,461,517,573)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =14 WHERE id IN (14,70,126,182,238,294,350,406,462,518,574)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =15 WHERE id IN (15,71,127,183,239,295,351,407,463,519,575)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =16 WHERE id IN (16,72,128,184,240,296,352,408,464,520,576)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =17 WHERE id IN (17,73,129,185,241,297,353,409,465,521,577)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =18 WHERE id IN (18,74,130,186,242,298,354,410,466,522,578)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =19 WHERE id IN (19,75,131,187,243,299,355,411,467,523,579)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =20 WHERE id IN (20,76,132,188,244,300,356,412,468,524,580)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =21 WHERE id IN (21,77,133,189,245,301,357,413,469,525,581)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =22 WHERE id IN (22,78,134,190,246,302,358,414,470,526,582)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =23 WHERE id IN (23,79,135,191,247,303,359,415,471,527,583)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =24 WHERE id IN (24,80,136,192,248,304,360,416,472,528,584)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =25 WHERE id IN (25,81,137,193,249,305,361,417,473,529,585)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =26 WHERE id IN (26,82,138,194,250,306,362,418,474,530,586)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =27 WHERE id IN (27,83,139,195,251,307,363,419,475,531,587)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =28 WHERE id IN (28,84,140,196,252,308,364,420,476,532,588)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =29 WHERE id IN (29,85,141,197,253,309,365,421,477,533,589)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =30 WHERE id IN (30,86,142,198,254,310,366,422,478,534,590)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =31 WHERE id IN (31,87,143,199,255,311,367,423,479,535,591)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =32 WHERE id IN (32,88,144,200,256,312,368,424,480,536,592)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =33 WHERE id IN (33,89,145,201,257,313,369,425,481,537,593)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =34 WHERE id IN (34,90,146,202,258,314,370,426,482,538,594)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =35 WHERE id IN (35,91,147,203,259,315,371,427,483,539,595)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =36 WHERE id IN (36,92,148,204,260,316,372,428,484,540,596)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =37 WHERE id IN (37,93,149,205,261,317,373,429,485,541,597)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =38 WHERE id IN (38,94,150,206,262,318,374,430,486,542,598)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =39 WHERE id IN (39,95,151,207,263,319,375,431,487,543,599)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =40 WHERE id IN (40,96,152,208,264,320,376,432,488,544,600)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =41 WHERE id IN (41,97,153,209,265,321,377,433,489,545,601)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =42 WHERE id IN (42,98,154,210,266,322,378,434,490,546,602)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =43 WHERE id IN (43,99,155,211,267,323,379,435,491,547,603)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =44 WHERE id IN (44,100,156,212,268,324,380,436,492,548,604)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =45 WHERE id IN (45,101,157,213,269,325,381,437,493,549,605)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =46 WHERE id IN (46,102,158,214,270,326,382,438,494,550,606)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =47 WHERE id IN (47,103,159,215,271,327,383,439,495,551,607)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =48 WHERE id IN (48,104,160,216,272,328,384,440,496,552,608)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =49 WHERE id IN (49,105,161,217,273,329,385,441,497,553,609)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =50 WHERE id IN (50,106,162,218,274,330,386,442,498,554,610)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =51 WHERE id IN (51,107,163,219,275,331,387,443,499,555,611)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =52 WHERE id IN (52,108,164,220,276,332,388,444,500,556,612)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =53 WHERE id IN (53,109,165,221,277,333,389,445,501,557,613)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =54 WHERE id IN (54,110,166,222,278,334,390,446,502,558,614)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =55 WHERE id IN (55,111,167,223,279,335,391,447,503,559,615)")
	cursor.execute("UPDATE SurfMaster2 SET Time_ID =56 WHERE id IN (56,112,168,224,280,336,392,448,504,560,616)")
	cursor.execute("ALTER TABLE SurfMaster2 ADD date_ TEXT")
	cursor.execute("UPDATE SurfMaster2 SET date_ = date('now') WHERE Time_ID BETWEEN 1 AND 8")
	cursor.execute("UPDATE SurfMaster2 SET date_ = date('now','+1 day') WHERE Time_ID BETWEEN 9 AND 16")
	cursor.execute("UPDATE SurfMaster2 SET date_ = date('now','+1 day') WHERE Time_ID = 9")
	cursor.execute("UPDATE SurfMaster2 SET date_ = date('now','+2 day') WHERE Time_ID BETWEEN 17 AND 24")
	cursor.execute("UPDATE SurfMaster2 SET date_ = date('now','+3 day') WHERE Time_ID BETWEEN 25 AND 32")
	cursor.execute("UPDATE SurfMaster2 SET date_ = date('now','+4 day') WHERE Time_ID BETWEEN 33 AND 40")
	cursor.execute("UPDATE SurfMaster2 SET date_ = date('now','+5 day') WHERE Time_ID BETWEEN 41 AND 48")
	cursor.execute("UPDATE SurfMaster2 SET date_ = date('now','+6 day') WHERE Time_ID BETWEEN 49 AND 56")
	cursor.execute("ALTER TABLE SurfMaster2 ADD time_ TEXT")
	cursor.execute("UPDATE SurfMaster2 SET time_ = '12am' WHERE Time_ID in (1,9,17,25,33,41,49)")
	cursor.execute("UPDATE SurfMaster2 SET time_ = '3am' WHERE Time_ID in (2,10,18,26,34,42,50)")
	cursor.execute("UPDATE SurfMaster2 SET time_ = '6am' WHERE Time_ID in (3,11,19,27,35,43,51)")
	cursor.execute("UPDATE SurfMaster2 SET time_ = '9am' WHERE Time_ID in (4,12,20,28,36,44,52)")
	cursor.execute("UPDATE SurfMaster2 SET time_ = '12pm' WHERE Time_ID in (5,13,21,29,37,45,53)")
	cursor.execute("UPDATE SurfMaster2 SET time_ = '3pm' WHERE Time_ID in (6,14,22,30,38,46,54)")
	cursor.execute("UPDATE SurfMaster2 SET time_ = '6pm' WHERE Time_ID in (7,15,23,31,39,47,55)")
	cursor.execute("UPDATE SurfMaster2 SET time_ = '9pm' WHERE Time_ID in (8,16,24,32,40,48,56)")
	conn.commit()
	cursor.close()
	conn.close()
	
my_function()
my_function2()
my_function3()
my_function4()
my_function5()

	#Executing this script should give us 616 rows