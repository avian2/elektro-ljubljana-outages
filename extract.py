import glob
import re

import datetime
import time

rows = []

for path in glob.glob("scrape/*aspx*"):
	n = None
	tn = None
	ltn = None
	dt = None

	for line in open(path):

		g = re.search('<p class="Datum">([0-9]+).([0-9]+).2014</p>', line)
		if g:
			day = int(g.group(1))
			month = int(g.group(2))

		g = re.search('<h2>([0-9]+)[.:]([0-9]+) - [Mm]otena oskrba', line)
		if g:
			hour = int(g.group(1))
			minute = int(g.group(2))

			dt = datetime.datetime(2014, month, day, hour, minute)

		g = re.search('([0-9.]+)(?:</?strong>| )+odjemalc', line)
		if g:
			n = g.group(1)
			n = n.replace('.', '')
			n = int(n)

		g = re.search('<p.*[^0-9]([0-9.]+)(?:</?strong>| )+transformatorskih', line)
		if g:
			tn = g.group(1)
			tn = tn.replace('.', '')
			tn = int(tn)

		g = re.search('Logatca ([0-9]+) transformatorskih', line)
		if g:
			ltn = g.group(1)
			ltn = ltn.replace('.', '')
			ltn = int(ltn)

	rows.append((dt, n, tn, ltn, path))


rows.sort()

for dt, n, tn, ltn, path in rows:
	print( "#", path)
	print( "#", dt)
	print( time.mktime(dt.timetuple())+3600.0, n, tn, ltn)
