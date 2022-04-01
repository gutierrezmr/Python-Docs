from impala.dbapi import connect
import pandas as pd
# Set Pyspark Python to Python 3
import os
import pyspark
from pyspark.sql import SparkSession, SQLContext
os.environ['PYSPARK_PYTHON'] = '/apps/Anaconda3.6/Anaconda3/bin/python3'
 
 
# Start Spark Session, Enable Arrow, and Define Impala Connection
!pip3 install pyarrow --upgrade
 
 
spark = SparkSession.builder \
.appName("Compliance Test") \
.getOrCreate()
 
spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
conn = connect(host='host', use_ssl=True,
             port='port', auth_mechanism='GSSAPI')
cursor = conn.cursor()
