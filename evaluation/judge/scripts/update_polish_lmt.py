import pandas as pd
import pymysql
import re
from glob import glob

rootdir="/home/judge/polish_limit/"
csv_files=glob(rootdir+"performance_*.csv")

df_list = []
for csv in csv_files:
    df_list.append(pd.read_csv(csv))
df = pd.concat(df_list, ignore_index=True)


df = df.groupby("problem_id").apply(lambda x: x.tail(7)).reset_index(drop=True)
df["time"]=df["time"].astype(int)
df["memory"]=df["memory"].astype(int)

aggresult = df.groupby("problem_id").agg(topmemory=("memory", "mean"), 
                                     total_time=("time", "mean"),
                                     memstd=("memory", "std"),
                                     timestd=("time", "std"), 
                                     count=("time", "count"))

config_path = "/home/judge/etc/judge.conf"
virtual_path = "/var/www/virtual/"
# Function to extract value from config file
def get_config_value(keyword):
    with open(config_path, 'r') as config_file:
        for line in config_file:
            if keyword in line:
                return re.search(r'=(.*)', line).group(1).strip()
# Extracting values from config file
server = get_config_value('OJ_HOST_NAME')
user = get_config_value('OJ_USER_NAME')
password = get_config_value('OJ_PASSWORD')
database = get_config_value('OJ_DB_NAME')
port = int(get_config_value('OJ_PORT_NUMBER'))
mysql_command = "mysql -h {} -P {} -u {} -p{} {}".format(server, port, user, password, database)
conn = pymysql.connect(host=server, port=port, user=user, password=password, database=database)
cursor = conn.cursor()

for problem_id, row in aggresult.iterrows():
    newmem=row["topmemory"]
    newtime=row["total_time"]
    newmem_std=row['memstd']
    newtime_std=row['timestd']
    sql = """
    SELECT time_limit,memory_limit,contest_id FROM problem where problem_id = {};
    """.format(problem_id)
    cursor.execute(sql)
    time_limit,memory_limit,contest_id = cursor.fetchall()[0]
    print("update time(ms)",time_limit,"to",newtime,"update mem(kb)",memory_limit,"to",newmem)

    sql = """
    UPDATE problem SET time_limit={}, memory_limit={} ,memstd = {} , timestd={} where problem_id = {};
    """.format(newtime,newmem,newmem_std,newtime_std,problem_id)
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
            print(e)
            conn.rollback()
    sql = """
    SELECT time_limit,memory_limit FROM problem where problem_id = {};
    """.format(problem_id)
    cursor.execute(sql)
    time_limit,memory_limit = cursor.fetchall()[0]

cursor.close()
conn.close()

