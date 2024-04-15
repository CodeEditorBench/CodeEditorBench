import openai
from openai import OpenAI
import pdb
from api_handler import api_handler
import json

def generate_prompt_debug(data, type='zero'):
    error_code = data['incorrect_solutions']
    code_language = data['code_language']
    public_tests_input = data['public_tests_input']
    public_tests_output = data['public_tests_output']
    if type == 'zero':
        prompt = f'''
### Instruction:
Please correct the errors in the buggy code snippet below, ensuring that your corrected code adheres to the specified programming language syntax and logic requirements. Validate your solution against the provided test cases to ensure its accuracy. Note that your solution should strictly consist of the corrected code only.
'''
    elif type == 'three':
        with open(f'few_shot_prompt/close/prompt_debug.txt', 'r') as f:
            prompt = f.read()
    else:
        raise NotImplementedError
    prompt += f'''
### Question:
Below is the {code_language} buggy code:
{error_code}

Correct the code and ensure it passes the following test case:
Input: {public_tests_input}
Output: {public_tests_output}

### Answer:
        '''
    return prompt


def generate_prompt_translate(data, type='zero'):
    source_code = data['source_code']
    source_lang = data['source_lang']
    target_lang = data['target_lang']
    public_tests_input = data['public_tests_input']
    public_tests_output = data['public_tests_output']
    if type == 'zero':
        prompt = f'''
### Instruction:
Please translate the following code snippet to another programming language, ensuring that your translated code meets the syntax and logic requirements of the target programming language. Validate your solution against the provided test cases to confirm its accuracy. Note that your submission should strictly contain the translated code only. 
'''
    elif type == 'three':
        with open(f'few_shot_prompt/close/prompt_translate.txt', 'r') as f:
            prompt = f.read()
    else:
        raise NotImplementedError
    prompt += f'''
### Question:
Below is the source code snippet in {source_lang}:
{source_code}

Translate this code to {target_lang}. Ensure your translated code works correctly with the test case provided:
Input: {public_tests_input}
Output: {public_tests_output}

### Answer:
    '''
    return prompt   


def generate_prompt_polishment(data, type='zero'):
    source_code = data['source_code']
    public_tests_input = data['public_tests_input']
    public_tests_output = data['public_tests_output']
    if type == 'zero':
        prompt = f'''
### Instruction:
Please optimize the given code snippet to enhance its execution efficiency and reduce memory usage, while ensuring the accuracy of the code remains unaffected. Validate your solution against the provided test cases to ensure its accuracy. Note that your submission should strictly consist of the optimized code only.
'''
    elif type == 'three':
        with open(f'few_shot_prompt/close/prompt_polishment.txt', 'r') as f:
            prompt = f.read()
    else:
        raise NotImplementedError
    prompt += f'''
### Question:
Below is the source code snippet that needs optimization:
{source_code}

Optimize the code and ensure it passes the following test case:
Input: {public_tests_input}
Output: {public_tests_output}

### Answer:
    '''
    return prompt


def generate_prompt_switch(data, type='zero'):
    similar_source_code = data['similar_source_code']
    public_similar_tests_input = data['public_similar_tests_input']
    public_similar_tests_output = data['public_similar_tests_output']
    public_target_tests_input = data['public_target_tests_input']
    public_target_tests_output = data['public_target_tests_output']
    if type == 'zero':
        prompt = f'''
### Instruction:
Please modify the given code snippet to implement a new function that is related to the original function implemented by the code. Ensure your modified code adheres to the programming language's syntax and logic requirements. Validate your solution against the provided test cases to ensure its accuracy. Your submission should strictly consist of the target code only.
'''
    elif type == 'three':
        with open(f'few_shot_prompt/close/prompt_switch.txt', 'r') as f:
            prompt = f.read()
    else:
        raise NotImplementedError
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
    '''
    return prompt


def generate_cot_prompt_debug(data):
    error_code = data['incorrect_solutions']
    code_language = data['code_language']
    public_tests_input = data['public_tests_input']
    public_tests_output = data['public_tests_output']
    prompt = f'''
### Instruction:
Please correct the buggy {code_language} code snippet below by using a step-by-step reasoning process, similar to how a large language model thinks. Follow these steps:

1. **Error Identification**: First, let's identify the errors in the code. Briefly describe what each error is and why it's a problem.

2. **Logical Reasoning**: For each identified error, use logical reasoning to explain how it impacts the code's functionality. This helps in understanding the nature of the problem.

3. **Solution Strategy**: Outline a strategy to correct the errors. This includes the steps you will take and the programming concepts you will apply to ensure the code meets the logic and syntax requirements of {code_language}.

4. **Implementation**: Provide the corrected code snippet based on your strategy. Make sure the code is syntactically correct and logically sound.

5. **Validation**: Validate your corrected code against the provided test case. Explain how the input leads to the expected output with your corrections.

### Question:
Below is the {code_language} buggy code snippet to correct:
{error_code}

Ensure your corrected code works correctly by testing it with this input and verifying it produces the expected output.
- Input: {public_tests_input}
- Output: {public_tests_output}

### Answer:

1. **Error Identification**: [Your identification and description of the errors] (Limit your response to 150 words)

2. **Logical Reasoning**: [Your reasoning on how each error affects the code] (Limit your response to 150 words)

3. **Solution Strategy**: [Outline of your strategy to correct the errors] (Limit your response to 150 words)

4. **Implementation**: [Your corrected code snippet]

5. **Validation**: [Explanation on how the input leads to the expected output with your corrections]
'''
    return prompt


def generate_cot_prompt_translate(data):
    source_code = data['source_code']
    source_lang = data['source_lang']
    target_lang = data['target_lang']
    public_tests_input = data['public_tests_input']
    public_tests_output = data['public_tests_output']
    prompt = f'''
### Instruction:
Please translate the following {source_lang} code snippet to {target_lang} by employing a step-by-step reasoning process, tailored to how a large language model would approach the task. Follow these steps:

1. **Functionality and Logic Analysis**: Begin with a thorough analysis of the source code's functionality and logic. Identify key programming constructs and logic flows used in the {source_lang} code.

2. **Identify Differences**: Highlight the syntactical and paradigmatic differences between {source_lang} and {target_lang}. Discuss how these differences might affect the translation of the code's logic and functionality.

3. **Translation Strategy**: Develop a detailed strategy for translating the source code into the target language. This should include a step-by-step plan that considers the identified differences and outlines how to adapt the source code's logic to fit the syntax and paradigms of {target_lang}.

4. **Implementation**: Translate the code according to your strategy. Ensure that the translated code not only syntactically correct but also preserves the original logic and functionality.

5. **Validation**: Validate your translated code using the provided test case. Explain the reasoning behind how the translated code produces the expected output given the input.

### Question:
Below is the {source_lang} code snippet to translate:
{source_code}

Test your translation with this input to ensure it produces the correct output.
- Input: {public_tests_input}
- Output: {public_tests_output}

### Answer:

1. **Functionality and Logic Analysis**: [Your analysis of the source code's functionality and logic] (Limit your response to 150 words)

2. **Identify Differences**: [Your discussion on the differences between {source_lang} and {target_lang}] (Limit your response to 150 words)

3. **Translation Strategy**: [Your detailed translation strategy] (Limit your response to 150 words)

4. **Implementation**: [Your translated code snippet]

5. **Validation**: [Your explanation on how the input leads to the expected output with your translation]
'''
    return prompt


def generate_cot_prompt_polishment(data):
    source_code = data['source_code']
    public_tests_input = data['public_tests_input']
    public_tests_output = data['public_tests_output']
    prompt = f'''
### Instruction:
Optimize the given code snippet for better execution efficiency and reduced memory usage by employing a step-by-step reasoning process. Follow these steps:

1. **Performance and Memory Analysis**: Start by thoroughly analyzing the source code to identify any performance bottlenecks and areas with excessive memory usage. Consider both the complexity of algorithms and the data structures used.

2. **Identify Optimization Opportunities**: Highlight specific lines of code or constructs that are inefficient. Explain why they are problematic and how they contribute to lower performance or higher memory usage.

3. **Optimization Strategies**: Develop a detailed plan for optimizing the code. This should include algorithmic improvements, data structure optimizations, and any coding practices that can enhance efficiency. Explain how each change is expected to improve performance or reduce memory usage.

4. **Implementation**: Apply your optimization strategies to modify the source code. Ensure that these changes maintain the code's accuracy and functionality.

5. **Validation**: Validate the optimized code using the provided test case. Detail how the optimizations impact the execution efficiency and memory usage in the context of the test case.

### Question:
Below is the code snippet that needs optimization:
{source_code}

Use this input to test your optimized code and confirm it produces the expected output.
- Input: {public_tests_input}
- Output: {public_tests_output}

### Answer:

1. **Performance and Memory Analysis**: [Your analysis of the code's performance and memory usage] (Limit your response to 150 words)

2. **Identify Optimization Opportunities**: [Specific inefficiencies and their impacts] (Limit your response to 150 words)

3. **Optimization Strategies**: [Your detailed plan for optimizing the code] (Limit your response to 150 words)

4. **Implementation**: [Your optimized code snippet]

5. **Validation**: [Explanation of how the optimizations improved efficiency or reduced memory usage]
'''
    return prompt


def generate_cot_prompt_switch(data):
    similar_source_code = data['similar_source_code']
    public_similar_tests_input = data['public_similar_tests_input']
    public_similar_tests_output = data['public_similar_tests_output']
    public_target_tests_input = data['public_target_tests_input']
    public_target_tests_output = data['public_target_tests_output']
    prompt = f'''
### Instruction:
Modify the following code snippet to implement a new specified function, using a step-by-step reasoning process. The process involves analyzing the current code's functionality, identifying necessary changes for the new requirements, and implementing these changes effectively. Follow these steps:

1. **Current Functionality Analysis**: Begin by thoroughly understanding and analyzing the functionality and logic of the current code. Identify the key operations and how they contribute to producing the given output.

2. **Identify New Requirements**: Compare the current functionality with the new function requirements. Highlight the differences in input and output specifications and any additional functionalities that need to be incorporated.

3. **Determine Required Changes**: Based on the analysis, specify the changes needed to adapt the existing code to the new requirements. This includes altering existing logic, adding new logic or functions, and removing unnecessary parts.

4. **Modification Strategy**: Develop a detailed plan for making these changes. This should outline any new algorithms, data structures, or coding constructs required to implement the new functionality while maintaining code efficiency and readability.

5. **Implementation**: Modify the source code according to your strategy. Ensure that the new code accurately implements the desired function and adheres to good coding practices.

6. **Validation**: Validate your modified code using the provided test case. Explain how the new input leads to the expected output, demonstrating the effectiveness of your modifications.

### Question:
Below is the code snippet that needs modification:
{similar_source_code}

It currently performs this operation:
- Input: {public_similar_tests_input}
- Output: {public_similar_tests_output}

Modify the code to achieve the following new functionality:
- Input: {public_target_tests_input}
- Output: {public_target_tests_output}

### Answer:

1. **Current Functionality Analysis**: [Your analysis of the source code's current functionality] (Limit your response to 150 words)

2. **Identify New Requirements**: [The differences between current and new requirements] (Limit your response to 150 words)

3. **Determine Required Changes**: [Specific changes needed for the new functionality] (Limit your response to 150 words)

4. **Modification Strategy**: [Your plan for implementing these changes] (Limit your response to 150 words)

5. **Implementation**: [The modified code snippet]

6. **Validation**: [Explanation of how the modifications meet the new requirements]
'''
    return prompt


def read_jsonl_file(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data


if __name__ == '__main__':
    api_handler = api_handler('gpt-35-turbo')
    data = read_jsonl_file('data/code_debug.jsonl')
    prompt = generate_cot_prompt_switch(data[0])

    max_tokens = 1024
    output_text = api_handler.get_output(input_text=prompt, max_tokens=max_tokens)
    print("Input:\n", prompt)
    print("Output:\n", output_text)
