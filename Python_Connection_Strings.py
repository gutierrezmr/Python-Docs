#Connecting to AWS
import getpass 
import psycopg2 
rs_dbhost = 'redshift.amazonaws.com' 
rs_dbport = 'port' 
rs_dbname = 'dbname' 
rs_dbuser = 'username' 
rs_dbpassword = 'password' #import getpass to pass pswd 
rs_conn = psycopg2.connect( 
    host=rs_dbhost, 
    user=rs_dbuser, 
    port=rs_dbport, 
    password=rs_dbpassword, 
    dbname=rs_dbname
) 
rs_cursor = rs_conn.cursor()

query = """
SQL query here
"""
#Read into pandas df
df = pd.read_sql(sql = query, con =rs_conn, index_col=None)

#-----------------------------

#Connecting to HUE
#Need to create ODBC connection for DB prior to connecting

import pyodbc
pyodbc.autocommit=True
conn=pyodbc.connect('DSN=NAME OF ODBC PROFILE', autocommit=True)
pd.read_sql('SHOW TABLES IN table', conn) #or read table into pandas df
