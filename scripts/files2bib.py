#!/usr/bin/env python
import sys
import glob
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def process_authors(authors):
    return (' '.join(' and '.join(strip_tags(authors).split(',')).split())).replace(' and and ',' and ')

def parse(fname):
    data={}
    f=open(fname)
    for line in f.readlines()[1:-1]:
        v=line.partition(':')
        data[v[0].strip()]=v[2][:-1]

    return """@article{%s,
  author  = {%s},
  title   = {%s},
  journal = {%s},
  month   = {%s},
  year    = {%s},
  url     = {%s}
}\n"""%(fname.split('/')[-1].split('.')[0],
        process_authors(data['authors']),
        data['title'],
        data['journal'],
        data['date'].split('/')[0],
        data['date'].split('/')[1],
        data['paper-url'],)
    

def write_bib():

    f=open(path+bibname,'w')

    for filename in glob.glob(path+'*.md'):
        print filename
        f.write(parse(filename))

    f.close()

path='./_publications/'
bibname='publications.bib'
authorname='J.R. Percival'

if __name__=="__main__":

    write_bib()
