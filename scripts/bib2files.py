#!/usr/bin/env python
import sys
import bibtexparser


def process_authors(authors):
    return ' and'.join((', '.join(authors.split(' and ')).replace(authorname,'<strong>'+authorname+'</strong>')).rsplit(',',1))

def write_files():
    with open(path+bibname) as bibtex_file:
        bibtex_str = bibtex_file.read()

        bib_database = bibtexparser.loads(bibtex_str)
        for entry in bib_database.entries:
            f=open(path+entry['ID']+'.md','w')
            print path+entry['ID']+'.md'
            f.write("""---
title: %s
authors: %s
journal: %s
paper-url: %s
date: %s/%s
---"""%(entry['title'],
        process_authors(entry['author']),
        entry['journal'],
        entry['link'],
        entry['month'],entry['year']))
            f.close()




path='./_publications/'
bibname='publications.bib'
authorname='J.R. Percival'

if __name__=="__main__":

    write_files()
