import pyodbc 
import pandas as pd
import time

SERVER = '192.168.50.10\WINCC'
DATABASE = 'IIT300'
USERNAME = 'bhipl'
PASSWORD = 'bhipl100'
connectionString = f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD};'
conn = pyodbc.connect(connectionString)
print("connection established!")
cursor = conn.cursor()	

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

prev_pressure = 0
while True:
    cursor.execute("SELECT top 2 * FROM [IIT300].[dbo].[ActualLog] where date1 = '2024-07-22' order by time1 desc") 
    row = cursor.fetchone() 
    data = []
    while row:
        row = cursor.fetchone()
        if row:
            data.append(row)

    for row in data:
        date = row[MAP.index('DATE1')]
        time_ = row[MAP.index('TIME1')]
        
        hp = row[MAP.index("HYDPRESSURE1")]
        hp += row[MAP.index("HYDPRESSURE2")]
        hp += row[MAP.index("HYDPRESSURE3")]
        hp += row[MAP.index("HYDPRESSURE4")]
        hp += row[MAP.index("HYDPRESSURE5")]
        hp += row[MAP.index("HYDPRESSURE6")]
        
        hp = hp/6
        
        deviation = prev_pressure - hp
        prev_pressure = hp
        print(date,time_,round(hp,2),round(deviation,2))
        time.sleep(1)
    
cursor.close()
conn.close()

