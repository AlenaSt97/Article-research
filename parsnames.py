import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import re
import sqlite3

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter URL name: ')
number=input('Enter article number')
html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

art=soup.find('article')
txt = art.get_text()
lenght=len(txt)
koeff=lenght/100000

bigcounts=dict()
def cellcounter(cells):
    counts=0
    count=txt.count(cells)+txt.count(cells.lower())
    counts=counts+count
    if counts>0:
        bigcounts[cells]=counts

headercounts=dict()
keywcounts=dict()
def strongarguments(cells):
    head=soup.find('h1')
    header=head.get_text()
    counts1=0
    matches1=re.findall(cells,header) or re.findall(cells.lower(),header)
    if len(matches1)>0:
        count1=header.count(cells)+header.count(cells.lower())
        counts1=counts1+count1
        if counts1>0:
            headercounts[cells]=counts1

    try:
        keyw = soup.find(class_="kwd-text")
        keywords=keyw.get_text()
        counts2=0
        matches2=re.findall(cells,keywords) or re.findall(cells.lower(),keywords)
        if len(matches2)>0:
            count2=keywords.count(cells)+keywords.count(cells.lower())
            counts2=counts2+count2
            if counts2>0:
                keywcounts[cells]=counts2
        return keywcounts
    except:
        keywcounts=dict()

    global strongdict
    strongdict=dict()
    strongdict={**headercounts,**keywcounts}

conn = sqlite3.connect('cell lines.db')
cur = conn.cursor()

cur.execute('SELECT Cell, Markers, Names FROM cell_lines')
while True:
    row=cur.fetchone()
    if row is None:
        break
    names=row[2].split(', ')
    for name in names:
        cellcounter(name)
        strongarguments(name)

print('strong cell names argument=',strongdict)

rating={k: bigcounts[k] for k in sorted(bigcounts, reverse=True, key=bigcounts.get)}
print(rating)

cur.execute('SELECT Cell, Markers, Names FROM cell_lines')
namestatus=dict()
while True:
    row=cur.fetchone()
    if row is None:
        break
    elmt=row[2].split(', ')
    initname=row[0]
    sumrate=list()
    for k,v in rating.items():
        if k in elmt:
            if k in strongdict.keys():
                sumrate.append(int(v)*1.3)
            else:                                   
                sumrate.append(int(v))
        else:
            continue
    if sum(sumrate)>0:
        namestatus[initname]=round(sum(sumrate)*koeff*10)
cellrating={k: namestatus[k] for k in sorted(namestatus, reverse=True, key=namestatus.get)}
print(cellrating)

cur.execute('SELECT Cell, Markers, Names FROM cell_lines')
allcells=list()
while True:
    row=cur.fetchone()
    if row is None:
        break
    allcells.append(row[0])

cur.close()

conn_1 = sqlite3.connect('markersrating.sqlite')
cur_1 = conn_1.cursor()

cur_1.execute('DROP TABLE IF EXISTS CellnameRating')

cur_1.execute('''CREATE TABLE IF NOT EXISTS CellnameRating
    (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, hypothesis_2 TEXT, Value TEXT)''')

for k,v in cellrating.items():
    cur_1.execute('''INSERT OR IGNORE INTO CellnameRating (hypothesis_2, Value)
    VALUES (?, ?)''', (k, v))

conn_1.commit()
cur_1.close()

conn_2 = sqlite3.connect('markersrating.sqlite')
cur_2 = conn_2.cursor()

#cur_2.execute('DROP TABLE IF EXISTS FinalRating')

cur_2.execute('''CREATE TABLE IF NOT EXISTS FinalRating
    (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, CellNames TEXT UNIQUE)''')

for i in allcells:
    cur_2.execute('INSERT OR IGNORE INTO FinalRating (CellNames) VALUES (?)', (i,))

#cur_2.execute('ALTER TABLE FinalRating DROP COLUMN Article_'+number)
cur_2.execute('ALTER TABLE FinalRating ADD Article_'+number)

conn_2.commit()
cur_2.close()
    
