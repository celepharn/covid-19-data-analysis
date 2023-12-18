import json
import sqlite3
import urllib.request, urllib.parse, urllib.error

# Parsing the json file from the internet
url = 'https://data.cdc.gov/api/views/hk9y-quqm/rows.json'
uh = urllib.request.urlopen(url)
str_data = uh.read().decode()
js_data = json.loads(str_data)
print('Retrieved', len(str_data), 'characters.')
info = js_data['data']
print("Number of entries: ", len(info))

# Making our connections
conn = sqlite3.connect('covid.sqlite')
cur = conn.cursor()

# Defining our tables
cur.executescript('''
    DROP TABLE IF EXISTS Age;
    DROP TABLE IF EXISTS Month;
    DROP TABLE IF EXISTS Year;
    DROP TABLE IF EXISTS Cond;
    DROP TABLE IF EXISTS CondGroup;
    DROP TABLE IF EXISTS Member;

    CREATE TABLE Age (
        id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        age    TEXT UNIQUE
    );

    CREATE TABLE Month (
        id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        month   TEXT UNIQUE
    );

    CREATE TABLE Year (
        id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        year    TEXT UNIQUE
    );

    CREATE TABLE Cond (
        id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        cond    TEXT UNIQUE
    );

    CREATE TABLE CondGroup (
        id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        condgroup    TEXT UNIQUE
    );


    CREATE TABLE Member (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        age_id     INTEGER,
        month_id   INTEGER,
        year_id   INTEGER,
        cond_id   INTEGER,
        condgroup_id   INTEGER,
        role INTEGER
    )
''')

# Iterate through the data, extract the info and insert it into our db
for field in range(len(info)) :
    age = info[field][18];
    month = info[field][13];
    year = info[field][12];
    cond = info[field][16];
    condgroup = info[field][15];
    if age is None :
        age = "Empty"
    if month is None :
        month = "Empty"
    if year is None :
        year = "Empty"
    if cond is None :
        cond = "Empty"
    if condgroup is None :
        condgroup = "Empty"

    #----------------------------------------------#
    # Insert data into the Age table               #
    # and grab the foreign key of every data entry #
    #----------------------------------------------#
    cur.execute('''
        INSERT OR IGNORE INTO Age (age)
        values ( ? )''', ( age, ) )
    # insert or ignore to not have repeated users
    cur.execute('SELECT id FROM Age WHERE age = ? ', (age, ))
    age_id = cur.fetchone()[0]
    # grab the foreign key for our join table

    #----------------------------------------------#
    # Insert data into the Month table               #
    # and grab the foreign key of every data entry #
    #----------------------------------------------#
    cur.execute('''
        INSERT OR IGNORE INTO Month (month)
        values ( ? )''', ( month, ) )
    # insert or ignore to not have repeated users
    cur.execute('SELECT id FROM Month WHERE month = ? ', (month, ))
    month_id = cur.fetchone()[0]
    # grab the foreign key for our join table

    #----------------------------------------------#
    # Insert data into the Age table               #
    # and grab the foreign key of every data entry #
    #----------------------------------------------#
    cur.execute('''
        INSERT OR IGNORE INTO Year (year)
        values ( ? )''', ( year, ) )
    # insert or ignore to not have repeated users
    cur.execute('SELECT id FROM Year WHERE year = ? ', (year, ))
    year_id = cur.fetchone()[0]
    # grab the foreign key for our join table

    #----------------------------------------------#
    # Insert data into the Age table               #
    # and grab the foreign key of every data entry #
    #----------------------------------------------#
    cur.execute('''
        INSERT OR IGNORE INTO Cond (cond)
        values ( ? )''', ( cond, ) )
    # insert or ignore to not have repeated users
    cur.execute('SELECT id FROM Cond WHERE cond = ? ', (cond, ))
    cond_id = cur.fetchone()[0]
    # grab the foreign key for our join table

    #----------------------------------------------#
    # Insert data into the Age table               #
    # and grab the foreign key of every data entry #
    #----------------------------------------------#
    cur.execute('''
        INSERT OR IGNORE INTO CondGroup (condgroup)
        values ( ? )''', ( condgroup, ) )
    # insert or ignore to not have repeated users
    cur.execute('SELECT id FROM CondGroup WHERE condgroup = ? ', (condgroup, ))
    condgroup_id = cur.fetchone()[0]
    # grab the foreign key for our join table

    #----------------------------------------------#
    # Insert data into the join table              #
    # this are the two foreign keys we got earlier #
    #----------------------------------------------#
    cur.execute('''
        INSERT OR REPLACE INTO Member
        (age_id, month_id, year_id, cond_id, condgroup_id, role) VALUES (?, ?, ?, ?, ?, ?)''',
        (age_id, month_id, year_id, cond_id, condgroup_id, field) )

conn.commit() # commit the changes
