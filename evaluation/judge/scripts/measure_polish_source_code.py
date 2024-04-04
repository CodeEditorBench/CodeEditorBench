import pandas as pd
import pymysql
import re
import time
from tqdm import trange
import logging
import os
logging.basicConfig(level=logging.INFO)


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
# 建立与MySQL服务器的连接
mysql_command = "mysql -h {} -P {} -u {} -p{} {}".format(server, port, user, password, database)
# print(mysql_command)
conn = pymysql.connect(host=server, port=port, user=user, password=password, database=database)
cursor = conn.cursor()


count=0
waiting=0
num_test=20
os.makedirs("/home/judge/polish_limit",exist_ok=True)
while count<=num_test:
    logging.info(f"count:{count},waiting minutes:{waiting}")
    sql="""
    SELECT s.solution_id, s.problem_id, s.result
    FROM solution s 
    JOIN problem p ON s.problem_id = p.problem_id 
    WHERE s.model_id in (45,46,47,48) and s.contest_id=1002 and s.result<4;
    """
    cursor.execute(sql)
    results=cursor.fetchall()
    if count==0 or len(results)==0:
        if count>0:
            #export limit
            select_sql = """
            select s.problem_id,s.time,s.memory
            from solution s
            where s.model_id in (45,46,47,48) and s.contest_id=1002
            """
            cursor.execute(select_sql)
            performance=cursor.fetchall()
            performance=pd.DataFrame(performance)
            performance.columns=['problem_id','time','memory']
            logging.info(f"export time and memory, count={count}")
            performance.to_csv(f'/home/judge/polish_limit/performance_{count}.csv',index=False)
        if count<num_test:
            logging.info("update polish source code result to 0")
            updatesql = """
            UPDATE solution so
            join (
                SELECT s.solution_id, s.problem_id,s.result
                FROM solution s 
                JOIN problem p ON s.problem_id = p.problem_id 
                WHERE s.model_id in (45,46,47,48) and s.contest_id=1002
            ) AS subquery ON so.solution_id = subquery.solution_id
            SET so.result = 0;
            """
            cursor.execute(updatesql)
            try:
                conn.commit()
            except Exception as e:
                logging.info(e)
                conn.rollback()
        count+=1
    else:#wait 10 mins
        total_sleep_time = 5*60
        logging.info("Waiting completion of the judging task. \nIf the judged process is not currently running, kindly execute the command `nohup bash run_judge.sh > runlog.out 2>&1 &` to commence the judged process in the background.\nIf the judged process has already been launched, please disregard this prompt.\n")
        for _ in range(int(total_sleep_time)):
            time.sleep(1)
        waiting+=5
        logging.info("\n5 minutes passed\n")

# 关闭连接
cursor.close()
conn.close()

