import sqlite3

conn = sqlite3.connect('markersrating.sqlite')
cur = conn.cursor()

cur.execute('SELECT * FROM FinalRating')
cellvalues=dict()
while True:
    row=cur.fetchone()
    if row is None:
        break
    cellvalues[row[1]]=(row[2:])

cur.execute('PRAGMA table_info(FinalRating)')
columns=list()
while True:
    col=cur.fetchone()
    if col is None:
        break
    columns.append(col[1])
fhand=open('cellrating.js','w')
fhand.write("cellrating = [ ['Blood cell names'")
for column in columns[2:]:
    fhand.write(",'"+column+"'")
fhand.write("]")

for key,val in cellvalues.items():
    cell=key
    fhand.write(",\n['"+cell+"'")
    values=list(val)
    for value in values:
        if value is None:
            fhand.write(","+str(0))
        else:
            fhand.write(","+str(value))
    fhand.write("]")
        
fhand.write("\n];\n")
fhand.close()


