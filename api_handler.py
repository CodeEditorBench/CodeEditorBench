import openai
from openai import OpenAI
import time
from wrapt_timeout_decorator import timeout
import pdb

@timeout(10) # 10 seconds timeout
def generate_response(client, engine, input_text, max_tokens, temperature, frequency_penalty, presence_penalty, stop):
    print("Generating response for engine: ", engine)
    start_time = time.time()
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": input_text}
        ],
        model=engine,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=0.9,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=stop,
    )
    end_time = time.time()
    print('Finish!')
    print("Time taken: ", end_time - start_time)
    return response

class api_handler:
    def __init__(self, model):
        self.model = model
        if self.model == 'gpt-35-turbo':
            self.engine = 'gpt-3.5-turbo-0125' # up to Sep 2021
        elif self.model == 'gpt-4':
            self.engine = 'gpt-4-0613' # up to Sep 2021
        else:
            raise NotImplementedError
        self.client = OpenAI(
            api_key="Your key here",
            base_url="Your base url here"
        )
    
    def get_output(self, input_text, max_tokens, temperature=0, frequency_penalty=0, presence_penalty=0, stop=None):
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                response = generate_response(self.client, self.engine, input_text, max_tokens, temperature, frequency_penalty, presence_penalty, stop)
                if response.choices and response.choices[0].message and hasattr(response.choices[0].message, 'content'):
                    return response.choices[0].message.content
                else:
                    return "Error: Wrong response format."
            except (TimeoutError, openai.APITimeoutError, openai.APIError, openai.APIConnectionError, openai.RateLimitError) as error:
                    print(f'Attempt {attempt+1} of {max_attempts} failed with error: {error}')
                    if attempt == max_attempts - 1:
                        return "Error: Max attempts reached."

if __name__ == '__main__':
    api_handler = api_handler('gpt-35-turbo')
    input_text = "Hello, how are you?"
    max_tokens = 50
    output_text = api_handler.get_output(input_text=input_text, max_tokens=max_tokens)
    print(output_text)
