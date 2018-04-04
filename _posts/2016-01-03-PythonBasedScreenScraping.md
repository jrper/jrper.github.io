---
title: Screen Scraping with python.
tag: python
---

A simple script to screen scrape data from the CricInfo StatsGuru engine can be written in python using the lxml and requests modules. The code looks like

{% highlight python %} 
from lxml import html
import requests

data={}
for i in range(100):
    page = requests.get('http://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;filter=advanced;groupby=overall;orderby=runs;runsmax1=%d;runsmin1=%d;runsval1=runs;template=results;type=batting'%(i,i))
    tree = html.fromstring(page.content)
    data[i] = [x.text for x in tree.xpath('//tr[@class="data1"]')[0].getchildren()]
    print "%3d : %5s %4s"%( i, data[i][4], data[i][5])
{% endhighlight %}

This outputs a list of scores by batsmen in Tests, the number of innings achieving that score and the number of those innings which were undefeated (i.e. with the batsman not out). As an exercise, lets graph the results:

{% highlight python %}
import matplotlib
matplotlib.rcParams['text.usetex'] = False
import pylab
pylab.xkcd()
f = lambda x : eval(data[x][4])-eval(data[x][5])
x=range(100)
pylab.plot(x,map(f,x))
pylab.xlabel('Score')
pylab.ylabel('log of frequency')
pylab.title('logarithmic frequency of Test scores')
{% endhighlight %}

![alt text]({{ site.url }}/images/TestScores.png "Graph of Test scores")


