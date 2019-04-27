#from https://gist.github.com/jaychoo/4e3effdeed3672173b67


import psycopg2
import pprint


configuration = { 'dbname': 'DB',
                  'user':'User',
                  'pwd':'Pass',
                  'host':'Host',
                  'port':'5439'
                }




def create_conn(*args,**kwargs):

    config = kwargs['config']
    try:
        conn=psycopg2.connect(dbname=config['dbname'], host=config['host'], port=config['port'], user=config['user'], password=config['pwd'])
    except Exception as err:
        print(err.code, err)
    return conn


def select(*args,**kwargs):
    # need a connection with dbname=<username>_db
    cur = kwargs['cur']

    try:
        # retrieving all tables in my search_path
        cur.execute("""select tablename from pg_table_def""")
    except Exception as err:
            print(err.code,err)


    rows = cur.fetchall()
    for row in rows:
        print(row)


def createemp(*args,**kwargs):
    # need a connection with dbname=<username>_db
    cur = kwargs['cur']

    try:
        # retrieving all tables in my search_path
        cur.execute("""create table emp (empid int, empname varchar(80))""")
    except Exception as err:
            print(err.code,err)


def selectemp(*args,**kwargs):
    # need a connection with dbname=<username>_db
    cur = kwargs['cur']

    sql = """select * from emp"""

    try:
        # retrieving all tables in my search_path
        cur.execute(sql)
    except Exception as err:
            print(err.code,err)


    rows = cur.fetchall()
    for row in rows:
        print(row)


def insertemp(*args,**kwargs):
    # need a connection with dbname=<username>_db
    cur = kwargs['cur']

    sql = """INSERT INTO emp values (10, 'smith')"""

    try:
        cur.execute(sql)
    except Exception as err:
        print(err.code, err)



print('start')
# need to add incoming rule for security group created for VPC to allow for
# Inbound - custom TCP - port 5439 - 0.0.0.0/0


conn = create_conn(config=configuration)

print('start select')
cursor = conn.cursor()
select(cur=cursor)
cursor.close()
print('finish select')

print('start create')
cursor = conn.cursor()
createemp(cur=cursor)
cursor.close()
conn.commit()
print('finish create')


print('start insert')
cursor = conn.cursor()
insertemp(cur=cursor)
cursor.close()
conn.commit()
print('finish insert')

print('start select emp')
cursor = conn.cursor()
selectemp(cur=cursor)
cursor.close()
print('finish select emp')

conn.close()
