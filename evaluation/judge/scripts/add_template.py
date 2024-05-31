import json
import re
import pymysql
import os
from tqdm import tqdm
from tree_sitter import Language, Parser


# Declaring a CPP code parser
CPP_LANGUAGE = Language('/home/judge/build/my-languages.so', 'cpp')
cpp_parser = Parser()
cpp_parser.set_language(CPP_LANGUAGE)

# Declaring a Python code parser
PYTHON_LANGUAGE = Language('/home/judge/build/my-languages.so', 'python')
python_parser = Parser()
python_parser.set_language(PYTHON_LANGUAGE)

# Declaring a Java code parser
JAVA_LANGUAGE = Language('/home/judge/build/my-languages.so', 'java')
java_parser = Parser()
java_parser.set_language(JAVA_LANGUAGE)

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
# 建立与MySQL服务器的连接
mysql_command = "mysql -h {} -P {} -u {} -p{} {}".format(server, port, user, password, database)
print(mysql_command)
conn = pymysql.connect(host=server, port=port, user=user, password=password, database=database)
cursor = conn.cursor()

def read_jsonl_file(file_path):
    data = []  
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            json_object = json.loads(line)  
            data.append(json_object) 
    return data

def remove_no_function_code(language, code):
    if language == PYTHON_LANGUAGE:
        query_text_1 = '''
        (function_definition name: (identifier)@1 )
        '''
        tree = python_parser.parse(bytes(code, "utf8"))
        
    root_node = tree.root_node
    query_1 = language.query(query_text_1)
    
    functions_defined = [(node.text, node.parent.text, node.parent.start_point, node.parent.end_point) for node, _ in query_1.captures(root_node)]
    
    function_ranges = [(start_point[0], end_point[0]) for _, _, start_point, end_point in functions_defined]
    function_code = []
    
    code_lines = code.split('\n')
    judge_flag=False
    for i, line in enumerate(code_lines):
        if line.strip() == "class Solution:":
            function_code.append(line)
            judge_flag=True
            continue
        if judge_flag==False:
            function_code.append(line)
        else:
            in_function = False
            for start, end in function_ranges:
                if start <= i <= end:
                    in_function = True
                    break
            if in_function:
                function_code.append(line)
    
    updated_code = '\n'.join(function_code)
    
    return updated_code



def remove_main_code(language, code):
    if language == CPP_LANGUAGE:
        query_text_1 = '''
        (function_declarator
            declarator: (field_identifier)@1
        )
        '''
        tree = cpp_parser.parse(bytes(code, "utf8"))
        
    elif language == JAVA_LANGUAGE:    
        query_text_1 = '''
        (method_declaration name: (identifier)@1 )
        '''
        tree = java_parser.parse(bytes(code, "utf8"))
        
    root_node = tree.root_node
    query_1 = language.query(query_text_1)
    root_node = tree.root_node
    if language == CPP_LANGUAGE:
        functions_defined = [(node.text, node.parent.parent.text, node.parent.parent.start_point, node.parent.parent.end_point) for node, _ in query_1.captures(root_node)]
    else:
        functions_defined = [(node.text, node.parent.text, node.parent.start_point, node.parent.end_point) for node, _ in query_1.captures(root_node)]
    
    for fun_name, fun_body, start_point, end_point in functions_defined:
        if fun_name.decode('utf-8') == "main":
            code_lines = code.split('\n')
            del code_lines[start_point[0]:end_point[0]+1]
            updated_code = '\n'.join(code_lines)
            code=updated_code

    return code

def find_fun_name(language, code):
    if language == CPP_LANGUAGE:
        query_text_1 = '''
        (function_declarator
            declarator: (field_identifier)@1
        )
        '''
        query_text_2 = '''
        (call_expression function: (identifier)@2 )
        '''
        
        tree = cpp_parser.parse(bytes(code, "utf8"))
        
    elif language == JAVA_LANGUAGE:    
        query_text_1 = '''
        (method_declaration name: (identifier)@1 )
        '''
        query_text_2 = '''
        (method_invocation name: (identifier)@2 )
        '''
        tree = java_parser.parse(bytes(code, "utf8"))
    elif language == PYTHON_LANGUAGE:      
        query_text_1 = '''
        (function_definition name: (identifier)@1 )
        '''
        query_text_2 = '''
        (call function: (identifier)@2)
        (call function: attribute: (attribute (identifier)@2))
        '''
        tree = python_parser.parse(bytes(code, "utf8"))
        
    root_node = tree.root_node
    query_1 = language.query(query_text_1)
    query_2 = language.query(query_text_2)
    root_node = tree.root_node

    if language == CPP_LANGUAGE:
        functions_defined = [(node.text, node.parent.parent.text, node.parent.parent.start_byte, node.parent.parent.end_byte) for node, _ in query_1.captures(root_node)]
    else:
        functions_defined = [(node.text, node.parent.text, node.parent.start_byte, node.parent.end_byte) for node, _ in query_1.captures(root_node)]
    if len(functions_defined) == 1:
        return functions_defined[0][0].decode('utf-8')
    
    functions_info = []
    for fun_name, fun_body, start_byte, end_byte in functions_defined:
        calls_within_function = [node.text for node, _ in query_2.captures(root_node, start_byte=start_byte, end_byte=end_byte)]
        function_call_count = len(calls_within_function)  
        functions_info.append({
            "function_name": fun_name,
            "calls": calls_within_function,
            "call_count": function_call_count  
        })

    functions_names = []
    functions_called = []  
    
    for function_info in functions_info:
        function_name = function_info['function_name'].decode('utf-8')
        calls = function_info['calls']
        unique_calls = [call.decode('utf-8') for call in calls if call.decode('utf-8') != function_name]
        functions_called.extend(unique_calls)
        functions_names.append(function_name) 

    final_function_name = set(functions_names) - set(functions_called)
    if len(final_function_name) == 1:
        return list(final_function_name)[0]
    else:
        max_call_count = 0
        most_called_function_name = None
        for function_name in final_function_name:
            for function_info in functions_info:
                if function_info['function_name'].decode('utf-8') == function_name:
                    call_count = function_info['call_count']
                    if call_count > max_call_count:
                        max_call_count = call_count
                        most_called_function_name = function_name

        return most_called_function_name

additional_cpp_imports = [
    "#include <bits/stdc++.h>",
    "#include \"../leetcode_template/cpp/LeetcodeIO.h\"",
    "using namespace std;",
]

def add_cpp_solution_class(source_code):
    new_class = f"class Solution {{\npublic:\n{source_code} \n}};\n"
    return new_class 

def add_cpp_footer_code(source_code, function_name=None):

    footer_code = """
int main() {{
    REGISTER_CONSTRUCTOR_SOLUTION;
    REGISTER_MEMBERFUNCTION_SOLUTION({});
    while (true) {{
        executor.constructSolution();
        executor.executeSolution();
    }}
}}
""".format(function_name).strip()

    source_code += "\n" + footer_code

    return source_code

def process_cpp_code(code):
    lines = code.split('\n')
    include_lines = [
    line for line in lines
    if line.strip() != '' and ("#include" in line or "using namespace" in line)
    and "#include <iostream>" not in line  
    ]

    include_code = '\n'.join(include_lines)

    for additional_import in additional_cpp_imports:
        if additional_import not in include_code:
            include_code += '\n' + additional_import
    
    filtered_lines = [
    line for line in lines
    if line.strip() != '' and ("#include" not in line and "using namespace" not in line)
    ]

    function_code = '\n'.join(filtered_lines)
    
    code_parts = []
    current_part = []

    for line in function_code.split('\n'):
        if line != '}' and line != '};':
            current_part.append(line)
        else:
            current_part.append(line)
            code_parts.append(current_part)
            current_part = []
    if current_part:
        code_parts.append(current_part)
          
    solution_code_part=""
    add_solution_flag = True
    multi_class = 0
    class_pattern = re.compile(r'(class|struct)\s+(\w+)')
    
    for part in code_parts:
        part_str = '\n'.join(part)
        class_match = class_pattern.search(part_str)
        if class_match:
            class_type = class_match.group(1)
            class_name = class_match.group(2)
            if class_name == "Node" or class_name == "ListNode" or class_name == "TreeNode":
                pass
            elif  class_name=="Solution":
                add_solution_flag = False
                solution_code_part = solution_code_part + '\n'.join(part) + "\n"
            else:
                multi_class+=1
        else:
            solution_code_part = solution_code_part + '\n'.join(part) + "\n"

    if add_solution_flag:
        solution_code_part = add_cpp_solution_class(solution_code_part)

    processed_code = include_code+"\n\n"+solution_code_part
    processed_code=remove_main_code(CPP_LANGUAGE, processed_code)
    return processed_code,multi_class

additional_java_imports = [
    "import com.template.Node;",
    "import com.template.ListNode;",
    "import com.template.TreeNode;",
    "import com.template.ParseInputUtil;",
    "import java.lang.reflect.Method;",
    "import java.lang.reflect.Type;",
    "import java.util.*;"
]
def add_java_solution_class(source_code):
    new_class = f"class Solution {{\n{source_code} \n}};\n"
    return new_class    

def add_java_footer_code(source_code, function_name=None):     
    footer_code = """
public class Main
{{
    public static void main( String[] args )
    {{
        String methodName = "{}";

        Scanner scanner = new Scanner(System.in);
        Method[] methods = Solution.class.getMethods();
        Method method = null;
        int numberOfParams = 0;
        for (Method method_check : methods) {{
            if (method_check.getName().equals(methodName)) {{
                method = method_check;
                Type[] genericParameterTypes = method.getGenericParameterTypes();
                numberOfParams = genericParameterTypes.length;
                break;
            }}
        }}
        
        while(scanner.hasNext()) {{
            List<String> stringParams = new ArrayList<String>();
            for (int i = 0; i < numberOfParams; i++) {{
                String line = scanner.nextLine();
                stringParams.add(line);
            }}
            Solution s = new Solution();
            try {{
                Type[] genericParameterTypes = method.getGenericParameterTypes();
                List<Object> parsedParams = new ArrayList<>();
                for (int i = 0; i < genericParameterTypes.length; i++) {{
                    Type paramType = genericParameterTypes[i];
                    String stringParam = stringParams.get(i);
                    if (stringParam.contains("None")) {{
                        stringParam = stringParam.replace("None", "null");
                    }}
                    Object parsedParam = ParseInputUtil.parseStringToType(stringParam, paramType);
                    parsedParams.add(parsedParam);
                }}
                Object result = method.invoke(s, parsedParams.toArray());
                System.out.println(result);
            }} catch (Exception e) {{
                e.printStackTrace();
            }}
        }}
        scanner.close();
    }}
}}
""".format(function_name).strip()
    source_code += "\n" + footer_code

    return source_code

def process_java_code(code):
    lines = code.split('\n')
    import_lines = [
    line for line in lines
    if line.strip() != '' and "import" in line and not line.strip().startswith("import java.util.")
    ]
    import_code = '\n'.join(import_lines)

    for additional_import in additional_java_imports:
        if additional_import not in import_code:
            import_code += '\n' + additional_import
    
    filtered_lines = [
        line for line in lines
        if line.strip() != '' and "import" not in line
    ]
    function_code = '\n'.join(filtered_lines)
    
    code_parts = []
    current_part = []

    for line in function_code.split('\n'):
        if line != '}':
            current_part.append(line)
        else:
            current_part.append(line)
            code_parts.append(current_part)
            current_part = []
    if current_part:
        code_parts.append(current_part)
          
    solution_code_part=""
    add_solution_flag = True
    multi_class = 0
    class_pattern = re.compile(r'class\s+(\w+)')
    for part in code_parts:
        part_str = '\n'.join(part)
        part_str = part_str.replace("public class", "class")
        class_match = class_pattern.search(part_str)
        if class_match:
            class_name = class_match.group(1)
            if class_name == "Node" or class_name == "ListNode" or class_name == "TreeNode":
                pass
            elif  class_name=="Solution":
                add_solution_flag = False
                solution_code_part = solution_code_part + part_str + "\n"
            else:
                multi_class+=1
        else:
            if not part[0].strip().startswith("public"):
                part[0] = "public " + part[0].lstrip()
            solution_code_part = solution_code_part + '\n'.join(part) + "\n"

    if add_solution_flag:
        solution_code_part = add_java_solution_class(solution_code_part)

    
    processed_code = import_code+"\n\n"+solution_code_part
    processed_code=remove_main_code(JAVA_LANGUAGE, processed_code)
    return processed_code,multi_class

additional_python_imports = [
    "import json",
    "import sys",
    "from parse_input import *",
    "from leetcode_class import ListNode, Node, TreeNode",
    "from typing import List"
]

def add_blank(code):
    code = '\n'.join('    ' + line for line in code.splitlines())
    return code

def add_self_to_function(code):
    pattern = r"^\s{4}def\s+(\w+)\s*\((.*?)\)(?:\s*->\s*(\w+))?:"
    matches = re.findall(pattern, code, re.MULTILINE)
    modified_code = code
    function_names=[]
    for match in matches:
        function_name = match[0]
        function_names.append(function_name)
        parameters = match[1].strip()
        return_type = match[2] if match[2] else ""
        if "self" not in parameters.split(","):
            if return_type:
                modified_code = modified_code.replace("def {}({}) -> {}:".format(function_name, parameters, return_type),
                                                  "def {}(self, {}) -> {}:".format(function_name, parameters, return_type))
            else:
                modified_code = modified_code.replace("def {}({}):".format(function_name, parameters),
                                                      "def {}(self, {}):".format(function_name, parameters))
    
    for function_name in function_names:
        pattern = rf"(\s*)(?<!\bself\.){function_name}\((?!self\s*,)"
        modified_code = re.sub(pattern, rf"\1self.{function_name}(", modified_code)
    return modified_code

def add_python_solution_class(source_code):
    new_class = f"class Solution:\n{source_code}"
    return new_class

def add_python_footer_code(source_code, function_name=None, func_input_type_list=None):
    footer_code = """
if __name__ == '__main__':
    object_func_name = {}
    func_input_type_list = {}

    while True:
        try:
            input_data = []
            for _ in range(len(func_input_type_list)):
                input_data.append(input())
            input_argus = []
            for input_data_item, input_data_type in zip(input_data, func_input_type_list):
                input_argus.append(parse_function_map[input_data_type](input_data_item))
            s = Solution()
            func = getattr(s, object_func_name)
            output = func(*input_argus)
            print(output)
        except EOFError:
            break
""".strip()

    if function_name:
        footer_code = footer_code.format(repr(function_name), repr(func_input_type_list))

    source_code += "\n\n" + footer_code

    return source_code

def process_python_code(code):
    lines = code.split('\n')
    import_lines = [
        line.strip().lstrip()  
        for line in lines
        if line.strip() != '' and "import" in line
    ]

    import_code = '\n'.join(import_lines)

    for additional_import in additional_python_imports:
        if additional_import not in import_code:
            import_code += '\n' + additional_import
    
    
        header_code = """
parse_function_map = {
    "'Node'": parse_node,
    "'Optional[Node]'": parse_node,
    "'TreeNode'": parse_treeNode,
    "ListNode": parse_listNode,
    "List['Node']": parse_list_node,
    "List[List[int]]": parse_list_list_int,
    "List[List[str]]": parse_list_list_str,
    "List[Optional[ListNode]]": parse_list_listNode,
    "List[TreeNode]": parse_list_treeNode,
    "List[bool]": parse_list_bool,
    "List[float]": parse_list_float,
    "List[int]": parse_list_int,
    "List[str]": parse_list_str,
    "Optional['Node']": parse_node,
    "Optional[ListNode]": parse_listNode,
    "Optional[TreeNode]": parse_treeNode,
    "TreeNode": parse_treeNode,
    "bool": parse_bool,
    "float": parse_float,
    "int": parse_int,
    "str": parse_str,
    "treeNode": parse_treeNode,
}
""".strip()

    filtered_lines = [
        line for line in lines
        if line.strip() != '' and "import" not in line
    ]
    function_code = '\n'.join(filtered_lines)
    
    code_parts = []
    current_part = []

    part_flag=False
    for line in function_code.split('\n'):
        if  not line.startswith(" "):
            part_flag = not part_flag
        if part_flag:
            current_part.append(line)
        else:
            code_parts.append(current_part)
            current_part = []
            current_part.append(line)
            part_flag = not part_flag
            
            
    if current_part:
        code_parts.append(current_part)
        
    solution_code_part=""
    add_solution_flag = True
    multi_class = 0
    class_pattern = re.compile(r'class\s+(\w+)')
    for part in code_parts:
        part_str = '\n'.join(part)
        class_match = class_pattern.search(part_str)
        if class_match:
            class_name = class_match.group(1)
            if class_name == "Node" or class_name == "ListNode" or class_name == "TreeNode":
                pass
            elif  class_name=="Solution":
                add_solution_flag = False
                if solution_code_part=="":
                    solution_code_part +='\n'.join(part)
                else:
                    solution_code_part = solution_code_part+"\n\n"+'\n'.join(part)
                break
            else:
                multi_class+=1
        else:
            if solution_code_part=="":
                solution_code_part +='\n'.join(part)
            else:
                solution_code_part = solution_code_part+"\n\n"+'\n'.join(part)

    if add_solution_flag:
        solution_code_part = add_blank(solution_code_part)
        solution_code_part = add_python_solution_class(solution_code_part)
        solution_code_part = add_self_to_function(solution_code_part)

    processed_code = import_code+"\n\n"+ header_code+ "\n\n"+ solution_code_part
    processed_code=remove_no_function_code(PYTHON_LANGUAGE, processed_code)
    
    return processed_code,multi_class


with open("/home/judge/scripts/idx_problem.jsonl","r") as dicf:
    idx_problem=json.load(dicf)
output_folder="/home/judge/solution_folder/processed_solution"
os.makedirs(output_folder,exist_ok=True)
language_map={"c++":"C++","cpp":"C++","java":"Java","python":"Python","python3":"Python"}

model_names=[x.replace(".jsonl","") for x in os.listdir(f"/home/judge/solution_folder/code_debug")]
for model_name in model_names:
    folders=["code_debug","code_polishment","code_switch","code_translate"]
    idxprefixes=["Code_Debug","Code_Polishment","Code_Switch","Code_Translate"]
    output_file=os.path.join(output_folder,model_name+".jsonl")
    with open(output_file,"w+",encoding="utf-8") as outf:
        count=0
        nosolution_num=0
        for folder,idxprefix in zip(folders,idxprefixes):
            ori_solution=f"/home/judge/solution_folder/{folder}/{model_name}.jsonl"
            print("processing",ori_solution)
            if os.path.exists(ori_solution):
                with open(ori_solution,"r",encoding="utf-8") as f:
                    for line in tqdm(f):
                        if count==0:
                            metadata={"model_name":model_name,"model_size":None,"model_url":None,
                            # "greedy_search_decoding":"Y","do_sample":"N",
                            # "num_output": 1, "temperature": 0
                            }
                            outf.write(json.dumps(metadata))
                            outf.write("\n")
                        if "model" in json.loads(line):
                            count+=1
                            continue
                        else:
                            inp=json.loads(line)
                            # print(inp.keys())
                            """
                            dict_keys(['num', 'title', 'difficulty', 'source_code', 'scource_lang', 
                            'average_running_time', 'average_memory', 
                            'public_tests_input', 'public_tests_output', 'private_tests_input', 'private_tests_output'])
                            """
                            newoutput={}
                            idx = f'{idxprefix}_{inp["problem_id"]}'
                            newoutput["problem_id"]=idx_problem[idx]
                            newoutput["completion_id"]=inp["completion_id"]
                            if "language" in inp:
                                inplang=inp["language"]
                            else:
                                inplang=inp["target_lang"]
                            if inplang not in language_map.values():
                                newoutput["language"]=language_map[inplang]
                            else:
                                newoutput["language"]=inplang
                            code1=inp["code"][0]
                            newoutput['ori_code']=inp["code"]
                            newoutput['code']=code1
                            geleetcode_sql="select leetcode from problem where problem_id=%s"
                            cursor.execute(geleetcode_sql,newoutput["problem_id"])
                            fetched=cursor.fetchall()
                            if len(fetched)==0:#跳过被删除的题目
                                count+=1
                                continue
                            is_leetcode=fetched[0][0]
                            if is_leetcode!='Y':#非leetcode题不用加模板
                                outf.write(json.dumps(newoutput))
                                outf.write("\n")
                                count+=1  
                            else:#leetcode题加模板
                                getfun_sql="select leetcode_fun_name from problem where problem_id=%s"
                                cursor.execute(getfun_sql,newoutput["problem_id"])
                                leetcode_fun_name=cursor.fetchall()[0][0]
                                code=code1
                                language=newoutput["language"]
                                # result.append(data)
                                MultiClass = 0
                                newoutput.update({"note": 0, "MultiClass": MultiClass, "is_same_name":1, "old_fun_name": None,"new_fun_name": None})
                                
                                if language == "C++":
                                    code = code.replace("private", "public")
                                    processed_code, MultiClass = process_cpp_code(code)
                                    newoutput["MultiClass"] = MultiClass
                                    
                                    function_name = find_fun_name(CPP_LANGUAGE, processed_code)
                                    if function_name == leetcode_fun_name:
                                        cpp_fun_name = leetcode_fun_name
                                        newoutput["is_same_name"] = 1
                                    else:
                                        cpp_fun_name = function_name
                                        newoutput["is_same_name"] = 0
                                    newoutput["old_fun_name"] = leetcode_fun_name
                                    newoutput["new_fun_name"] = cpp_fun_name
                                    
                                    final_code=add_cpp_footer_code(processed_code, function_name)
                                    
                                    if newoutput["MultiClass"]==0:
                                        newoutput["code"] = final_code
                                            
                                elif language == "Java":
                                    
                                    code = code.replace("private", "public")
                                    processed_code, MultiClass = process_java_code(code)
                                    newoutput["MultiClass"] = MultiClass
                                    
                                    function_name = find_fun_name(JAVA_LANGUAGE, processed_code)
                                    if function_name == leetcode_fun_name:
                                        java_fun_name = leetcode_fun_name
                                        newoutput["is_same_name"] = 1
                                    else:
                                        java_fun_name = function_name
                                        newoutput["is_same_name"] = 0
                                    newoutput["old_fun_name"] = leetcode_fun_name
                                    newoutput["new_fun_name"] = java_fun_name
                                    
                                    final_code = add_java_footer_code(processed_code, function_name)
                                    
                                    if newoutput["MultiClass"]==0:
                                        newoutput["code"] = final_code

                                elif language == "Python":
                                    gettype_sql="select leetcode_fun_input_type from problem where problem_id=%s"
                                    cursor.execute(gettype_sql,newoutput['problem_id'])
                                    leetcode_fun_input_type=cursor.fetchall()[0][0]

                                    code = code.replace("private", "public")
                                    processed_code, MultiClass = process_python_code(code)
                                    newoutput["MultiClass"] = MultiClass
                                    
                                    function_name = find_fun_name(PYTHON_LANGUAGE, processed_code)
                                    if function_name == leetcode_fun_name:
                                        python_fun_name = leetcode_fun_name
                                        newoutput["is_same_name"] = 1
                                    else:
                                        python_fun_name = function_name
                                        newoutput["is_same_name"] = 0
                                    newoutput["old_fun_name"] = leetcode_fun_name
                                    newoutput["new_fun_name"] = python_fun_name
                                    
                                    final_code = add_python_footer_code(processed_code, function_name,leetcode_fun_input_type)
                                    if newoutput["MultiClass"]==0:
                                        newoutput["code"] = final_code
                
                                # newoutput["new_fun_name"]=list(newoutput["new_fun_name"])
                                # print("newoutput",newoutput)   
                                outf.write(json.dumps(newoutput))
                                outf.write("\n")
                                count+=1  
                                nosolution_num+=1
cursor.close()
conn.close()
