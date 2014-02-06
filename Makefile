all: publish

extract.csv: scrape extract.py
	python3 extract.py > extract.csv

extract.png: extract.csv extract.gnuplot
	gnuplot extract.gnuplot

publish: extract.png animation.gif
	scp extract.png cloudsdale.tablix.org:public_html/elektro.png
	scp animation.gif cloudsdale.tablix.org:public_html/elektro_anim.gif

anim/out: anim.py anim/label.png scrape
	rm -r anim/out
	mkdir anim/out
	python anim.py

animation.gif: anim/out
	convert -delay 10 -loop 0 `ls anim/out/*.png|head -n -1` -delay 400 `ls anim/out/*.png|tail -n1` $@

.PHONY: publish
