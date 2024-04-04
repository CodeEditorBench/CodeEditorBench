import pandas as pd
import pymysql
import re
from typing import List, Union
import numpy as np
import os

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


contest_map={1000:'code_debug',1001:'code_translation',1002:'code_polishment',
1003:'code_requirement_switch'}

def estimate_pass_at_k(
    num_samples: Union[int, List[int], np.ndarray],
    num_correct: Union[List[int], np.ndarray],
    k: int,
) -> np.ndarray:
    """
    Estimates pass@k of each problem and returns them in an array.
    """

    def estimator(n: int, c: int, k: int) -> float:
        """
        Calculates 1 - comb(n - c, k) / comb(n, k).
        """
        if n - c < k:
            return 1.0
        return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))

    if isinstance(num_samples, int):
        num_samples_it = itertools.repeat(num_samples, len(num_correct))
    else:
        assert len(num_samples) == len(num_correct)
        num_samples_it = iter(num_samples)

    return np.array(
        [estimator(int(n), int(c), k) for n, c in zip(num_samples_it, num_correct)]
    )

sql="""select model_id,model_name from models 
where 
model_id>48
"""
cursor.execute(sql)
to_parse=cursor.fetchall()

sql="""select model_id,model_name from models 
WHERE 
model_name LIKE 'resubmit%' OR model_name LIKE 'supplement%'
"""
cursor.execute(sql)
to_preplace=cursor.fetchall()

def update_result(row):
    if row["contest_id"]==1002:
        if row["result"]==4:
            row["time_limit"]=row["time_limit"]
            row["memory_limit"]=row["memory_limit"]
            time_pulish=0*row["timestd"]
            mem_pulish=0*row["memstd"]
            if _polish:
                if row["avg_time"]<row["time_limit"]-time_pulish and row["avg_memory"]<row["memory_limit"]-mem_pulish:
                    result=43
                elif row["avg_time"]<row["time_limit"]-time_pulish:
                    result=41
                elif row["avg_memory"]<row["memory_limit"]-mem_pulish:
                    result=42
                else:
                    result=44
                polish_score_time = (float(row["time_limit"]) - row["avg_time"]) / float(row["time_limit"])
                polish_score_mem=(row["memory_limit"]-row["avg_memory"])/row["memory_limit"]
                polish_score_total=max((polish_score_time+polish_score_mem)/2,0)
            else:
                result=4
                polish_score_time=None
                polish_score_mem=None
                polish_score_total=None
        else:
            result=row["result"]
            polish_score_time=0.0
            polish_score_mem=0.0
            polish_score_total=0.0
    else:#其他
        result=row["result"]
        polish_score_time=None
        polish_score_mem=None
        polish_score_total=None
    return [result,polish_score_time,polish_score_mem,polish_score_total]

def round_dict_values(d, decimals=4):
    return {k: round(v, decimals) if isinstance(v, (int, float)) else v for k, v in d.items()}

_polish=True
for _problems in ['plus','primary']:
    outresults={"model_name":[],
        "model_id":[],
        "solution_num":[],
        "passed_num":[],
        'code_debug':[],
        'code_translation':[],
        'code_requirement_switch':[],
        'code_polishment':[],
        'polish_score_total':[],
        }
    for model_id,model_name in to_parse:
        print(model_id,model_name)
        if _problems=='plus':
            sql="""
            SELECT p.problem_id,p.title,s.result,p.contest_id,solution_id,completion_id,s.time,s.memory,p.time_limit,p.memory_limit,p.timestd,p.memstd
            FROM solution s 
            JOIN problem p ON s.problem_id = p.problem_id 
            WHERE s.model_id=%s and p.defunct='N' and p.leetcode='Y' and result>=4 
            and result!=14
            """
        else:
            sql="""
            SELECT p.problem_id,p.title,s.result,p.contest_id,solution_id,completion_id,s.time,s.memory,p.time_limit,p.memory_limit,p.timestd,p.memstd
            FROM solution s 
            JOIN problem p ON s.problem_id = p.problem_id 
            WHERE s.model_id=%s and p.defunct='N' and result>=4 
            and result!=14
            """
        cursor.execute(sql,model_id)
        results=cursor.fetchall()
        if len(results)==0:
            continue
        columns = ['problem_id','title', 'result', 'contest_id', 'solution_id', 
                    'completion_id','time','memory','time_limit','memory_limit','timestd','memstd']
        df = pd.DataFrame(results, columns=columns)

        df_grouped = df.groupby(['title', 'completion_id'])
        avg_performance=df_grouped.agg({"time":np.mean,"memory":np.mean}).reset_index()
        avg_performance.rename(columns={"time": "avg_time", "memory": "avg_memory"}, inplace=True)
        df_with_aggregates = pd.merge(avg_performance, df[['title', 'completion_id','contest_id','result','time_limit','memory_limit','timestd','memstd']], on=['title', 'completion_id'], how='left')
        df_with_aggregates.drop_duplicates(subset=['title', 'completion_id'], keep='first', inplace=True)


        df_with_aggregates[['result','polish_score_time','polish_score_mem','polish_score_total']] = df_with_aggregates.apply(update_result, axis=1,result_type='expand')
        df_with_aggregates["pass"]=df_with_aggregates["result"].apply(lambda x: 1 if x in (4,41,42,43) else 0)
        if _polish:
            df_with_aggregates["polish_time"]=df_with_aggregates["result"].apply(lambda x: 1 if x==41 else 0)
            df_with_aggregates["polish_mem"]=df_with_aggregates["result"].apply(lambda x: 1 if x==42 else 0)
            df_with_aggregates["polish_both"]=df_with_aggregates["result"].apply(lambda x: 1 if x==43 else 0)
            df_with_aggregates["no_polish"]=df_with_aggregates["result"].apply(lambda x: 1 if x==44 else 0)
    
        outresults["model_name"].append(model_name)
        outresults["model_id"].append(model_id)
        outresults["solution_num"].append(df_with_aggregates["pass"].count())
        outresults["passed_num"].append(df_with_aggregates["pass"].sum())
        if _polish:
            outresults["polish_score_total"].append(df_with_aggregates["polish_score_total"].mean())

        for contest_id, group in df_with_aggregates.groupby('contest_id'):
            print("category:",contest_map[contest_id])
            df_by_problem=group.groupby(['title']).agg({"completion_id":"count","pass":"sum"})
            df_by_problem.rename(columns={"completion_id": "total", "pass": "correct"}, inplace=True)
            print("category solution num:\n",len(df_by_problem))
            pass_at_k = {
                f"pass@{k}": estimate_pass_at_k(df_by_problem["total"], df_by_problem["correct"], k).mean()
                for k in [1, 10, 20]
                if df_by_problem["total"].min() >= k
            }
            for k, v in pass_at_k.items():
                print(f"{k}:\t{v:.3f}")
            if len(pass_at_k.items())==1:
                outresults[contest_map[contest_id]].append(pass_at_k["pass@1"])
            else:
                outresults[contest_map[contest_id]].append(pass_at_k)
        unique_contest_ids = df_with_aggregates['contest_id'].unique()
        for contest_id,contest_name in contest_map.items():
            if contest_id not in unique_contest_ids:
                outresults[contest_map[contest_id]].append(None)
    print(outresults)
    outresults=pd.DataFrame(outresults)
    outresults[['code_debug','code_translation','code_polishment','code_requirement_switch']] = (
        outresults[['code_debug', 'code_translation', 'code_polishment', 'code_requirement_switch']]
        .applymap(lambda x: round_dict_values(x) if isinstance(x, dict) else x)
    )
    
    outresults["model_type"]="submitted"
    os.makedirs(f"/home/judge/metrics", exist_ok=True)
    if _problems=='plus' and _polish:
        outresults.to_csv(f"/home/judge/metrics/metrics_plus.csv")
    elif _problems=='primary' and _polish:
        outresults.to_csv(f"/home/judge/metrics/metircs_primary.csv")

cursor.close()
conn.close()

