import re
import sqlite3

number=input('Enter article number again')

conn = sqlite3.connect('markersrating.sqlite')
cur = conn.cursor()

cur.execute('SELECT id, hypothesis_1, Value FROM MarkersRating')
mrsstatus=dict()
while True:
    row=cur.fetchone()
    if row is None:
        break
    cellname=row[1]
    mrsrating=row[2]
    mrsstatus[cellname]=mrsrating

cur.close()

conn_1 = sqlite3.connect('markersrating.sqlite')
cur_1 = conn_1.cursor()

cur_1.execute('SELECT id, hypothesis_2, Value FROM CellnameRating')
namestatus=dict()
while True:
    row=cur_1.fetchone()
    if row is None:
        break
    cellsname=row[1]
    namerating=row[2]
    namestatus[cellsname]=namerating

cur_1.close()

finalstatus=mrsstatus
for k,v in finalstatus.items():
    if k in namestatus.keys():
        finalstatus[k]=(int(namestatus[k])+int(v))
    else:
        finalstatus[k]=int(v)
        
for key,val in namestatus.items():
    if key not in finalstatus.keys():
        finalstatus[key]=int(val)
    else:
        continue
        
finalrating={k: finalstatus[k] for k in sorted(finalstatus, reverse=True, key=finalstatus.get)}
print(finalrating)
    
conn_2 = sqlite3.connect('markersrating.sqlite')
cur_2 = conn_2.cursor()

for k,v in finalrating.items():
    cur_2.execute('UPDATE FinalRating SET Article_'+number+ '=(?) WHERE CellNames=(?)',(v,k))

conn_2.commit()
cur_2.close()
