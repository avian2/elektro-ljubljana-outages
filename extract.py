# -*- coding: utf8 -*-
import json
import glob
import re
import sys

import datetime

OBMOCJA = {
	u'bokalcev':		'bokalci',
	u'cerknice':		'cerknica',
	u'cerknice,':		'cerknica',
	u'črnomelj':		'crnomelj',
	u'črnomlja':		'crnomelj',
	u'črnuč':		'crnuce',
	u'dobrepolja':		'dobrepolje',
	u'domžal':		'domzale',
	u'grosuplja':		'grosuplje',
	u'kamnika':		'kamnik',
	u'kočevja':		'kocevje',
	u'litije':		'litija',
	u'(zapodje)':		'litija',
	u'logatca':		'logatec',
	u'mesta':		'novomesto',
	u'metlika':		'metlika',
	u'metlike':		'metlika',
	u'polje':		'polje',
	u'radeč':		'radece',
	u'radečah':		'radece',
	u'ribnice':		'ribnica',
	u'&scaron;entjerneja':	'sentjernej',
	u'&scaron;i&scaron;ke':	'siska',
	u'tacna':		'tacen',
	u'(vikr\u010de)':	'tacen',
	u'trbovelj':		'trbovlje',
	u'trbovlje':		'trbovlje',
	u'trebnjega':		'trebnje',
	u'vrhnike':		'vrhnika',
	u'zagorja':		'zagorje',
	u'zagradca':		'zagradec',
	u'zagradec':		'zagradec',
	u'zajasovnik)':		'zagorje',
	u'\u017eirov':		'ziri',
}

rows = []
a = set()

for path in glob.glob("scrape/*aspx*"):

	if path.endswith("Vse-novice.aspx"):
		continue

	row = {
			'datoteka': path,
			'tp_brez_napetosti': {},
	}

	start_list = False

	for line in open(path):

		g = re.search('<p class="Datum">([0-9]+).([0-9]+).2014</p>', line)
		if g:
			day = int(g.group(1))
			month = int(g.group(2))

		g = re.search('<h2>([0-9]+)[.:]([0-9]+) - [Mm]otena oskrba', line)
		if g:
			hour = int(g.group(1))
			minute = int(g.group(2))

			row['cas'] = datetime.datetime(2014, month, day, hour, minute).isoformat()

		g = re.search('([0-9.]+)(?:</?strong>| )+odjemalc', line)
		if g:
			if '<p>Z agregati' in line:
				continue

			n = g.group(1)
			n = n.replace('.', '')

			if 'odjemalci_brez_napetosti' not in row:
				row['odjemalci_brez_napetosti'] = int(n)

		g = re.search('<p.*[^0-9]([0-9.]+)(?:</?strong>|&nbsp;| )+transformatorskih', line)
		if g:
			n = g.group(1)
			n = n.replace('.', '')

			if not start_list and 'tp_brez_napetosti_skupaj' not in row:
				row['tp_brez_napetosti_skupaj'] = int(n)

		g = re.search(' ([^ ]+)(?: |&nbsp;)+([0-9]+)(?: |&nbsp;|TP)+transformatorsk', line)
		if g:
			start_list = True
			obmocje2 = g.group(1).decode('utf8').lower()
			n = int(g.group(2))

			obmocje = OBMOCJA.get(obmocje2)
			if obmocje is None:
				if obmocje2 not in a:
					print '\t%r:\t\t%r' % (obmocje2, obmocje2)
					a.add(obmocje2)
			else:
				row['tp_brez_napetosti'][obmocje] = n

	rows.append(row)

rows.sort(key=lambda x:x['cas'])
json.dump(rows, open(sys.argv[1], 'w'), indent=4)

#print( time.mktime(dt.timetuple())+3600.0, n, tn, ltn)
