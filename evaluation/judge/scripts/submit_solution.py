import pymysql
import re
import os
from tqdm import tqdm
import json

language_name=["C","C++","Pascal","Java","Ruby","Bash","Python","PHP","Perl","C#","Obj-C","FreeBasic","Scheme","Clang","Clang++","Lua","JavaScript","Go","SQL","Fortran","Matlab","Cobol","UnknownLanguage"]

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
print(mysql_command)
conn = pymysql.connect(host=server, port=port, user=user, password=password, database=database)
cursor = conn.cursor()

source_dir="/home/judge/log/new_outputs"
datadir="/home/judge/data"


solution_root="/home/judge/solution_folder/processed_solution"

for fname in os.listdir(solution_root):
    solution_dir=os.path.join(solution_root,fname)
    with open(solution_dir,"r") as f:
        user_id="admin"
        try:
            for count,line in tqdm(enumerate(f)):
                if not line.strip():
                    continue
                if count==0:
                    modelData = json.loads(line)
                    modelName = modelData['model_name']
                    modelSize = modelData.get('model_size',0)
                    greedy_search_decoding = modelData.get('greedy_search_decoding', 'N')
                    modelUrl = modelData.get('model_url',"")
                    doSample = modelData.get('do_sample', 'N')
                    temperature = modelData.get('temperature', 0.0)

                    # model exist:
                    sql = "SELECT `model_id` FROM `models` WHERE `model_name`=%s"
                    cursor.execute(sql, (modelName,))
                    result = cursor.fetchall()
                    if len(result)!=0:
                        print("skip existing model:",modelName)
                        break

                    try:
                        modelInsertQuery = "INSERT INTO models (user_id, model_name, size, model_url, greedy_search_decoding, do_sample, temperature) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                        cursor.execute(modelInsertQuery, (user_id,modelName,modelSize,modelUrl, greedy_search_decoding, doSample, temperature,))
                        print(modelInsertQuery)
                        model_id = cursor.lastrowid
                        print("model_id",model_id)
                    except Exception as e:
                        print(e)
                        raise Exception("Invalid Meta data")
                else:
                    # print(count)
                    solutionData=json.loads(line)
                    if solutionData is not None:
                        try:
                            # Insert data into the 'solution' table
                            problemId = solutionData['problem_id']
                            source = solutionData['code']
                            completion_id = solutionData['completion_id']
                            if source!=None:
                                length = len(source)
                            else:
                                continue
                            language = solutionData['language']
                            try:
                                lang = language_name.index(language)
                            except ValueError:
                                print(f"The language {language} is not supported.")
                                print("Supported languages are:")
                                print(language_name)
                                raise Exception("Invalid Language")

                            sql = "SELECT `contest_id`, `contest_name` FROM `problem` WHERE `problem_id`=%s"
                            cursor.execute(sql, (problemId,))
                            result = cursor.fetchall()
                            if len(result) == 0:
                                raise Exception(f"Can't find corresponding contest of problem_id {problemId}")
                            contest_id = result[0][0]
                            contest_name = result[0][1]
                            # print("contest_id",contest_id,"contest_name",contest_name)
                            # Calculate problem number in contest based on contest_name
                            num = None
                            inserttime=1
                            if contest_name == "code_debug":
                                sql = "SELECT `id` FROM code_debug WHERE `problem_id`=%s"
                            elif contest_name == "code_translation":
                                sql = "SELECT `id` FROM code_translation WHERE `problem_id`=%s"
                            elif contest_name == "code_polishment":
                                sql = "SELECT `id` FROM code_polishment WHERE `problem_id`=%s"
                                inserttime=2
                            elif contest_name == "code_requirement_switch":
                                sql = "SELECT `id` FROM code_requirement_switch WHERE `problem_id`=%s"
                            else:
                                raise Exception("Invalid contest_name")
                            cursor.execute(sql, (problemId,))
                            result = cursor.fetchall()
                            # print("result",result)
                            if result:
                                num = result[0][0]
                            for _ in range(inserttime):
                                try:
                                    # Inserting data into solution table
                                    sql = "INSERT INTO solution(model_id, problem_id, completion_id, user_id, submit_date, language, code_length, contest_id, num, result) VALUES(%s, %s, %s, %s, NOW(), %s, %s, %s, %s, 14)"
                                    cursor.execute(sql, (model_id, problemId, completion_id, user_id, lang, length, contest_id, num))
                                    solution_id = cursor.lastrowid
                                except Exception as e:
                                    raise e
                                try:
                                    # Inserting source code into source_code table
                                    codeInsertQuery = "INSERT INTO source_code (solution_id, source) VALUES (%s, %s)"
                                    cursor.execute(codeInsertQuery, (solution_id, source))
                                except Exception as e:
                                    raise e
                            try:
                                # Updating model table's submit count
                                sql = "UPDATE models SET submit = submit + 1 WHERE model_id = %s"
                                cursor.execute(sql, (model_id,))

                                # Updating problem table's submit count
                                sql = "UPDATE problem SET submit = submit + 1 WHERE problem_id = %s"
                                cursor.execute(sql, (problemId,))
                            except Exception as e:
                                raise e
                        except Exception as e:
                            print("Error:", str(e))
                            raise e
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e

cursor.close()
conn.close()

