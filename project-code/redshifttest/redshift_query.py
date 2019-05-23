#from https://gist.github.com/jaychoo/4e3effdeed3672173b67


import psycopg2
import pprint


# configuration = { 'dbname': 'devdb',
#                   'user':'awsuser',
#                   'pwd':'AWSPass321',
#                   'host':'cl1.crlmi1f9xwzi.us-east-1.redshift.amazonaws.com',
#                   'port':'5439'
#                 }


configuration = { 'dbname': 'db1',
                  'user':'awsuser',
                  'pwd':'AWSPass321',
                  'host':'cl6.ced9iqbk50ks.us-west-2.redshift.amazonaws.com',
                  'port':'5439'
                }

# cl3.ced9iqbk50ks.us-west-2.redshift.amazonaws.com:5439

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


def sql_in_file(*args,**kwargs):
    fd = open(kwargs['filename'], 'r')
    sql_file = fd.read()
    fd.close()

    # all SQL statements (split on ';')
    sql_stmts = sql_file.split(';')

    cur = kwargs['cur']

    currentconn = kwargs['conn']

    for stmt in sql_stmts:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        if stmt is None or len(stmt.strip()) == 0:
            continue
        try:
            cur.execute(stmt)
        except psycopg2.InterfaceError as err:
            print("error in interface:", err)
            currentconn.rollback()
            continue
        except psycopg2.DatabaseError as err:
            print("error related to DB:", err)
            currentconn.rollback()
            continue
        except psycopg2.DataError as err:
            print("error in data:", err)
            currentconn.rollback()
            continue
        except psycopg2.OperationalError as err:
            print("error related to db operation:", err)
            currentconn.rollback()
            continue
        except psycopg2.IntegrityError as err:
            print("error in data integrity:", err)
            currentconn.rollback()
            continue
        except psycopg2.InternalError as err:
            print("error: internal, usually type of DB Error:", err)
            currentconn.rollback()
            continue
        except psycopg2.ProgrammingError as err:
            print("error in Programming:", err)
            currentconn.rollback()
            continue
        except psycopg2.NotSupportedError as err:
            print("error - not supported feature/operation: ", err)
            currentconn.rollback()
            continue


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

# print('start select')
# cursor = conn.cursor()
# select(cur=cursor)
# cursor.close()
# print('finish select')
#
# print('start create')
# cursor = conn.cursor()
# createemp(cur=cursor)
# cursor.close()
# conn.commit()
# print('finish create')
#
#
# print('start insert')
# cursor = conn.cursor()
# insertemp(cur=cursor)
# cursor.close()
# conn.commit()
# print('finish insert')
#
# print('start select emp')
# cursor = conn.cursor()
# selectemp(cur=cursor)
# cursor.close()
# print('finish select emp')

print('start ddl file')
cursor = conn.cursor()
sql_in_file(filename = './redshiftddlfile.sql', cur=cursor, conn=conn)
cursor.close()
conn.commit()
print('finish ddl file')

conn.close()
