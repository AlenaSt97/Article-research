import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import re
import sqlite3

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter URL name: ')
html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

art=soup.find('article')
txt = art.get_text()
lenght=len(txt)
koeff=lenght/100000

bigcounts=dict()
def parsemarkers(markers):
    counts=dict()
    words=re.findall(markers,txt)
    if len(words)>0:
        for word in words:
            counts[word] = counts.get(word, 0) + 1
    if (len(counts))>0:
        bigcounts.update(counts)

headercounts=dict()
keywcounts=dict()
def strongarguments(markers):
    counts1=dict()
    head=soup.find('h1')
    header=head.get_text()
    matches1=re.findall(markers,header)
    if len(matches1)>0:
        for match1 in matches1:
            counts1[match1] = counts1.get(match1, 0) + 1
    if (len(counts1))>0:
        headercounts.update(counts1)

    try:
        counts2=dict()
        keyw = soup.find(class_="kwd-text")
        keywords=keyw.get_text()
        matches2=re.findall(markers,keywords)
        if len(matches2)>0:
            for match2 in matches2:
                counts2[match2] = counts2.get(match2, 0) + 1
        if (len(counts2))>0:
            keywcounts.update(counts2)
    except:
        keywcounts=dict()

def compensation(markersdict):
    global mrsdict
    mrsdict=dict()
    markersdict = {key:markersdict[key] for key in sorted(markersdict,reverse=True)}
    lkeys=list(markersdict.keys())
    skeys=(','.join(lkeys))
    for i in lkeys:
        compen=list()
        x=0
        if len(re.findall(i,skeys))>1:
            for k,v in markersdict.items():
                if i in k and i!=k:
                    compen.append(int(markersdict[k]))
                    x=sum(compen)
                if i in k and i==k and x!=0:
                    markersdict[k]=markersdict[k]-x

    for k,v in markersdict.copy().items():
        if v==0:
            del markersdict[k]
    mrsdict=markersdict

conn = sqlite3.connect('cell lines.db')
cur = conn.cursor()

cur.execute('SELECT Cell, Markers, Names FROM cell_lines')
while True:
    row=cur.fetchone()
    if row is None:
        break
    refs=row[1].split(', ')
    for mrs in refs:
        parsemarkers(mrs)
        strongarguments(mrs)

compensation(bigcounts)
bigcounts=mrsdict

compensation(headercounts)
headercounts=mrsdict

compensation(keywcounts)
keywcounts=mrsdict

strongdict={**headercounts,**keywcounts}
print('strong markers argument=',strongdict)

rating={k: bigcounts[k] for k in sorted(bigcounts, reverse=True, key=bigcounts.get)}
print('markers rating',rating)

cur.execute('SELECT Cell, Markers, Names FROM cell_lines')
cellstatus=dict()
while True:
    row=cur.fetchone()
    if row is None:
        break
    elements=row[1].split(', ')
    l=len(elements)
    cell=row[0]
    sumrate=list()
    for k,v in rating.items():
        if k in elements:
            if k in strongdict.keys():
                sumrate.append(int(v)*1.3)
            else:                                   
                sumrate.append(int(v))
        else:
            continue
    if sum(sumrate)>0:
        cellstatus[cell]=round(sum(sumrate)*100*koeff/l)

cellname=dict()
for k,v in cellstatus.copy().items():
        if v==0:
            del cellstatus[k]
cellname=cellstatus

cellrating={k: cellname[k] for k in sorted(cellname, reverse=True, key=cellname.get)}
print('summ cell markers',cellrating)


cur.close()

conn_1 = sqlite3.connect('markersrating.sqlite')
cur_1 = conn_1.cursor()

cur_1.execute('DROP TABLE IF EXISTS MarkersRating')

cur_1.execute('''CREATE TABLE IF NOT EXISTS MarkersRating
    (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, hypothesis_1 TEXT, Value TEXT)''')

for k,v in cellrating.items():
    cur_1.execute('''INSERT OR IGNORE INTO MarkersRating (hypothesis_1, Value)
    VALUES (?, ?)''', (k, v))

conn_1.commit()
cur_1.close()
