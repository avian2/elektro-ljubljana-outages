import re

fn = "scrape/Vse-novice.aspx"

for line in open(fn):
	
	g = re.search("(http://www.elektro-ljubljana.si/2/Za-medije/Vse-novice/Novica/articleType/ArticleView/articleId/[0-9]+/[0-9]+--Motena-oskrba-z-elektricno-energijo-zaradi-vremenskih-razmer.aspx)", line)

	if g:
		print g.group(1)
