import pyodbc
import pandas as pd
import time

SERVER = 'IIT300T,1433'
DATABASE = 'IIT300'
USERNAME = 'bhipl'
PASSWORD = 'bhipl100'
connectionString = f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD};'
conn = pyodbc.connect(connectionString)
print("connection established!")
cursor = conn.cursor()
from datetime import datetime

def get_time_seconds(time_str1, time_str2):
    if not time_str1 or not time_str2:
        return 0
    time_format = '%H:%M:%S'

    time1 = datetime.strptime(time_str1, time_format)
    time2 = datetime.strptime(time_str2, time_format)

    time_diff = (time2 - time1).total_seconds()
    return time_diff

MAP = [
"ID",
"DATE1",
"TIME1",
"BATCHNO",
"RECEIPENAME",
"ACKPOSITIONCH1",
"ACKPOSITIONCH2",
"ACKPOSITIONCH3",
"ACKPOSITIONCH4",
"ACKPOSITIONCH5",
"ACKPOSITIONCH6",
"ACKPOSITIONCH7",
"ACKPOSITIONCH8",
"HYDPRESSURE1",
"HYDPRESSURE2",
"HYDPRESSURE3",
"HYDPRESSURE4",
"HYDPRESSURE5",
"HYDPRESSURE6",
"HYDPRESSURE7",
"HYDPRESSURE8",
"VOLTAGE",
"ICURRENT",
"POWER",
"POWERSPARE1",
"CWTZ01",
"CWTZ02",
"CWTZ03",
"CWTZ04",
"CWTZ05",
"CWTZ06",
"CWTZ07",
"CWTZ08",
"ANVILTEMPZ01",
"ANVILTEMPZ02",
"ANVILTEMPZ03",
"ANVILTEMPZ04",
"ANVILTEMPZ05",
"ANVILTEMPZ06",
"ANVILTEMPZ07",
"ANVILTEMPZ08",
"POSWZ01",
"POSWZ02",
"POSWZ03",
"POSWZ04",
"POSWZ05",
"POSWZ06",
"POSWZ07",
"POSWZ08",
"PRESWZ01",
"PRESWZ02",
"PRESWZ03",
"PRESWZ04",
"PRESWZ05",
"PRESWZ06",
"PRESWZ07",
"PRESWZ08",
"COOLWZ01",
"COOLWZ02",
"COOLWZ03",
"COOLWZ04",
"COOLWZ05",
"COOLWZ06",
"COOLWZ07",
"COOLWZ08",
"ANILTEMPWZ01",
"ANILTEMPWZ02",
"ANILTEMPWZ03",
"ANILTEMPWZ04",
"ANILTEMPWZ05",
"ANILTEMPWZ06",
"ANILTEMPWZ07",
"ANILTEMPWZ08",
"ACKKW",
"ACKKWH",
"RECORDREF",
"OPERATORNAME",
"STIMEMINTOTAL",
"STIMEHH",
"STIMEMM",
"STIMESS",
"ACKSTEPNO",
"SERVOPRESSURESSET",
"SERVOFLOWSET",
"FRONTPOSITIONSET",
"REARPOSITIONSET",
"LEFTPOSITIONSET",
"RIGHTPOSITIONSET",
"TOPPOSITIONSET",
"BOTTOMPOSITIONSET",
"DOWELSET",
"ACKTOTTIMEDAYS",
"ACKTOTALTIMEHH",
"ACKTOTALTIMEMM",
"ACKTOTALTIMESS",
"TOTCOUNTERTIMESS"
]

prev_time = ''
this_time = ''
running_count  = 0
diff_count = 0
while True:
    cursor.execute("SELECT top 1 * FROM [IIT300].[dbo].[ActualLog] where date1 = '2024-11-06' order by time1 desc")
    row = cursor.fetchone()
    
    date = row[MAP.index('DATE1')]
    time_ = row[MAP.index('TIME1')].split('.')[0]
    this_time = date + "|" + time_
    diff = get_time_seconds(prev_time,time_)
    diff_count +=1
    running_count += diff
    average_diff = running_count/diff_count
    prev_time = time_
    hp =  row[MAP.index("HYDPRESSURE1")]
    hp += row[MAP.index("HYDPRESSURE2")]
    hp += row[MAP.index("HYDPRESSURE3")]
    hp += row[MAP.index("HYDPRESSURE4")]
    hp += row[MAP.index("HYDPRESSURE5")]
    hp += row[MAP.index("HYDPRESSURE6")]

    hp = hp/6
    print(this_time,hp,diff,average_diff)
    time.sleep(5)

cursor.close()
conn.close()
	