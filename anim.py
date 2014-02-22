# -*- coding: utf8 -*-
import glob
import json

import datetime
import time

import os.path
import sys

from PIL import Image, ImageFont, ImageDraw

SIZE=None
VIDEO_SIZE=(1280, 720)

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
		return (230, 230, 230)
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
rows = json.load(open("extract.json"))
for row in rows:
	row['cas'] = datetime.datetime(*time.strptime(row['cas'], "%Y-%m-%dT%H:%M:%S")[:6])

frow = dict(rows[0])
frow['cas'] -= datetime.timedelta(seconds=3600*12)
rows = [ frow ] + rows

prev_t = None
prev_im = None

cur_t = None

font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 14)
label = Image.open("anim/label.png")

canvas = Image.new("RGB", VIDEO_SIZE, "white")

offset = (
		(VIDEO_SIZE[0] - SIZE[0])/2,
		(VIDEO_SIZE[1] - SIZE[1])/2,
	)

cur_n = 0
for row in rows:
	obmocja = row['tp_brez_napetosti']
	if not obmocja:
		print "x"
		continue

	t = time.mktime(row['cas'].timetuple())
	im = composite(slides, obmocja)

	if cur_t is not None:
		while cur_t < t:
			im2 = Image.blend(prev_im, im, 1.0 - (t - cur_t)/(t - prev_t))

			cur_dt = datetime.datetime.fromtimestamp(cur_t+3600.0)

			draw = ImageDraw.Draw(im2)
			draw.text((7, 2), str(cur_dt), (0, 0, 0), font=font)

			im2 = Image.composite(label, im2, label)

			canvas.paste(im2, offset)

			canvas.save("anim/out/out-%04d.png" % cur_n)
			cur_n += 1

		
			cur_t += 1800
	else:
		cur_t = t

	prev_t = t
	prev_im = im

for n in xrange(40):
	canvas.save("anim/out/out-%04d.png" % cur_n)
	cur_n += 1
