all: publish

extract.json: scrape extract.py
	python extract.py $@

graph.csv: extract.json graph.py
	python graph.py > $@

graph.png: graph.csv graph.gnuplot
	gnuplot graph.gnuplot

publish: graph.png animation.mp4
	scp graph.png cloudsdale.tablix.org:public_html/elektro.png
	scp animation.mp4 cloudsdale.tablix.org:public_html/elektro_anim.mp4

anim/out: anim.py anim/label.png scrape
	rm -r anim/out
	mkdir anim/out
	python anim.py

animation.gif: anim/out
	convert -delay 10 -loop 0 `ls anim/out/*.png|head -n -1` -delay 400 `ls anim/out/*.png|tail -n1` $@

animation.mp4: anim/out
	rm -f animation.mp4
	avconv -r 15 -f image2 -c:v png -i "anim/out/out-%04d.png" -c:v libx264 $@

.PHONY: publish
