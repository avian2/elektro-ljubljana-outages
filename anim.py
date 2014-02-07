# -*- coding: utf8 -*-
import glob
import re

import datetime
import time

import os.path
import sys

from PIL import Image, ImageFont, ImageDraw

SIZE=None

OBMOCJA = {
	'ribnice': 'ribnica',
	'logatca': 'logatec',
	'vrhnike': 'vrhnika',
	'litije': 'litija',
	'zagorja': 'zagorje',
	'kamnika': 'kamnik',
	u'črnomlja': 'crnomelj',
	'cerknice': 'cerknica',
	'cerknice,': 'cerknica',
	u'domžal': 'domzale',
	u'kočevja': 'kocevje',
	u'radeč': 'radece',
	u'radečah': 'radece',
	'dobrepolja': 'dobrepolje',
	'trebnjega': 'trebnje',
	'zagradca': 'zagradec',
	u'črnuč': 'crnuce',
	'metlike': 'metlika',
	'&scaron;entjerneja': 'sentjernej',
	'grosuplja': 'grosuplje',
	'bokalcev': 'bokalci',
	'tacna': 'tacen',
	u'(vikr\u010de)': 'tacen',
	'zajasovnik)': 'zagorje',
	u'\u017eirov': 'ziri',
	'&scaron;i&scaron;ke': 'siska',
	'trbovelj': 'trbovlje',
	'mesta': 'novomesto',
	'(zapodje)': 'litija',
}

def load_slides():
	global SIZE
	slides = {}

	for path in glob.glob("anim/obmocja/*.png"):
		name = os.path.basename(path)[:-4]
		slides[name] = Image.open(path).convert("L")
		SIZE = slides[name].size

	return slides

def n_to_rgb(n):
	if n == 0:
		return (220, 220, 220)
	else:
		b = max(0, 200 - n*1)
		return (200, b, b)

def composite(slides, obmocja):
	im = Image.new("RGB", SIZE, "white")

	for name, slide in slides.iteritems():
		n = obmocja.pop(name, 0)

		rgb = n_to_rgb(n)
		im = Image.composite(im, Image.new("RGB", SIZE, rgb), slide)

	if obmocja:
		print obmocja
	else:
		print "ok"

	return im

slides = load_slides()

rows = []

for path in glob.glob("scrape/*aspx*"):
#for path in glob.glob("scrape/2000--*aspx*"):
	n = None
	tn = None
	ltn = None
	dt = None

	obmocja = {}

	for line in open(path):

		g = re.search('<p class="Datum">([0-9]+).([0-9]+).2014</p>', line)
		if g:
			day = int(g.group(1))
			month = int(g.group(2))

		g = re.search('<h2>([0-9]+)[:.]([0-9]+) - [mM]otena oskrba', line)
		if g:
			hour = int(g.group(1))
			minute = int(g.group(2))

			dt = datetime.datetime(2014, month, day, hour, minute)

		g = re.search(' ([^ ]+)(?: |&nbsp;)+([0-9]+)(?: |&nbsp;|TP)+transformatorsk', line)
		if g:
			obmocje2 = g.group(1).decode('utf8').lower()
			n = int(g.group(2))

			obmocje = OBMOCJA.get(obmocje2, obmocje2)
			obmocja[obmocje] = n

	rows.append((dt, obmocja))

rows.sort()

f = rows[1]
rows = [ (f[0] - datetime.timedelta(seconds=3600*12), {'b':0}) ] + rows[1:]

prev_t = None
prev_im = None

cur_t = None

font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 14)
label = Image.open("anim/label.png")

for dt, obmocja in rows:
	if not obmocja:
		print "x"
		continue

	t = time.mktime(dt.timetuple())
	im = composite(slides, obmocja)

	if cur_t is not None:
		while cur_t < t:
			im2 = Image.blend(prev_im, im, 1.0 - (t - cur_t)/(t - prev_t))

			cur_dt = datetime.datetime.fromtimestamp(cur_t+3600.0)

			draw = ImageDraw.Draw(im2)
			draw.text((7, 2), str(cur_dt), (0, 0, 0), font=font)

			im2 = Image.composite(label, im2, label)

			im2.save("anim/out/out-%d.png" % cur_t)
		
			cur_t += 1800
	else:
		cur_t = t

	prev_t = t
	prev_im = im
