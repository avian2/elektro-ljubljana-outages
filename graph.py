import json

import datetime
import time

for row in json.load(open("extract.json")):
	dt = datetime.datetime(*time.strptime(row['cas'], "%Y-%m-%dT%H:%M:%S")[:6])
	print time.mktime(dt.timetuple())+3600.0, row.get('odjemalci_brez_napetosti'), row.get('tp_brez_napetosti_skupaj'), row['tp_brez_napetosti'].get('logatec')
