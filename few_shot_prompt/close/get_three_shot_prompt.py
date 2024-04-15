import json

def three_shot_prompt_debug():
    prompt = f'''### Instruction: 
Please correct the errors in the buggy code snippet below, ensuring that your corrected code adheres to the specified programming language syntax and logic requirements. Additionally, validate your solution against the provided test cases to ensure its accuracy. Note that your solution should strictly consist of the corrected code only.
'''
    with open(f'cluster_{dataset}.jsonl', 'r') as f:
        for line in f:
            data = json.loads(line)
            error_code = data['incorrect_solutions']
            correct_code = data['solutions']
            code_language = data['code_language']
            public_tests_input = data['public_tests_input']
            public_tests_output = data['public_tests_output']
            prompt += f'''
### Question:
Below is the {code_language} buggy code:
{error_code}

Correct the code and ensure it passes the following test case:
Input: {public_tests_input}
Output: {public_tests_output}

### Answer:
{correct_code}
'''
    print(prompt)
    with open(f'prompt_{dataset}.txt', 'w') as f:
        f.write(prompt)


def three_shot_prompt_translate():
    prompt = f'''### Instruction: 
Please translate the following code snippet to another programming language, ensuring that your translated code meets the syntax and logic requirements of the target programming language. Validate your solution against the provided test cases to confirm its accuracy. Note that your submission should strictly contain the translated code only. 
'''
    with open(f'cluster_{dataset}.jsonl', 'r') as f:
        for line in f:
            data = json.loads(line)
            source_code = data['source_code']
            target_code = data['target_code']
            source_lang = data['source_lang']
            target_lang = data['target_lang']
            public_tests_input = data['public_tests_input']
            public_tests_output = data['public_tests_output']
            prompt += f'''
### Question:
Below is the source code snippet in {source_lang}:
{source_code}

Translate this code to {target_lang}. Ensure your translated code works correctly with the test case provided:
Input: {public_tests_input}
Output: {public_tests_output}

### Answer:
{target_code}
'''
    print(prompt)
    with open(f'prompt_{dataset}.txt', 'w') as f:
        f.write(prompt)


def three_shot_prompt_polishment():
    prompt = f'''### Instruction: 
Please optimize the given code snippet to enhance its execution efficiency and reduce memory usage, while ensuring the accuracy of the code remains unaffected. Validate your solution against the provided test cases to ensure its accuracy. Note that your submission should strictly consist of the optimized code only.
'''
    with open(f'cluster_{dataset}.jsonl', 'r') as f:
        for line in f:
            data = json.loads(line)
            source_code = data['source_code']
            efficient_code = data['efficient_code']
            public_tests_input = data['public_tests_input']
            public_tests_output = data['public_tests_output']
            prompt += f'''
### Question:
Below is the source code snippet that needs optimization:
{source_code}

Optimize the code and ensure it passes the following test case:
Input: {public_tests_input}
Output: {public_tests_output}

### Answer:
{efficient_code}
'''
    print(prompt)
    with open(f'prompt_{dataset}.txt', 'w') as f:
        f.write(prompt)


def three_shot_prompt_switch():
    prompt = f'''### Instruction: 
Please modify the given code snippet to implement a specified function, ensuring that your modified code meets the syntax and logic requirements of the programming language. Validate your solution against the provided test cases to ensure its accuracy. Your submission should strictly consist of the target code only.
'''
    with open(f'cluster_{dataset}.jsonl', 'r') as f:
        for line in f:
            data = json.loads(line)
            similar_source_code = data['similar_source_code']
            target_source_code = data['target_source_code']
            public_similar_tests_input = data['public_similar_tests_input']
            public_similar_tests_output = data['public_similar_tests_output']
            public_target_tests_input = data['public_target_tests_input']
            public_target_tests_output = data['public_target_tests_output']
            prompt += f'''
### Question:
Below is the code snippet that implements a specific function:
{similar_source_code}

It currently performs the operation:
Input: {public_similar_tests_input}
Output: {public_similar_tests_output}

You are required to modify this code to implement a new function that is related to the original one, as detailed below:
Input: {public_target_tests_input}
Output: {public_target_tests_output}

Ensure your modified code passes the provided test case.

### Answer:
{target_source_code}
'''
    print(prompt)
    with open(f'prompt_{dataset}.txt', 'w') as f:
        f.write(prompt)


def read_jsonl_file(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data

if __name__ == '__main__':
    dataset = 'debug'
    three_shot_prompt_debug()

    with open(f'prompt_{dataset}.txt', 'r') as f:
        prompt = f.read()
    print(prompt)
    