import json

import requests
import os
import time
import re

# For local streaming, the websockets are hosted without ssl - http://
HOST = '133.9.14.117:2500'
URI = f'http://{HOST}/api/v1/chat'

# For reverse-proxied streaming, the remote will likely host with ssl - https://
# URI = 'https://your-uri-here.trycloudflare.com/api/v1/chat'


def run(name,prompt, history,log_dir):
    request = {
        'user_input': prompt,
        'max_new_tokens': 500,
        'auto_max_new_tokens': False,
        'history': history,
        'mode': 'instruct',  # Valid options: 'chat', 'chat-instruct', 'instruct'
        'character': 'Example',
        'instruction_template': 'Vicuna-v1.1',  # Will get autodetected if unset
        'your_name': 'You',
        # 'name1': 'name of user', # Optional
        # 'name2': 'name of character', # Optional
        # 'context': 'character context', # Optional
        # 'greeting': 'greeting', # Optional
        # 'name1_instruct': 'You', # Optional
        # 'name2_instruct': 'Assistant', # Optional
        # 'context_instruct': 'context_instruct', # Optional
        # 'turn_template': 'turn_template', # Optional
        'regenerate': False,
        '_continue': False,
        'chat_instruct_command': 'Continue the chat dialogue below. Write a single reply for the character "<|character|>".\n\n<|prompt|>',

        # Generation params. If 'preset' is set to different than 'None', the values
        # in presets/preset-name.yaml are used instead of the individual numbers.
        'preset': 'None',
        'do_sample': True,
        'temperature': 0.7,
        'top_p': 0.1,
        'typical_p': 0.5,
        'epsilon_cutoff': 0,  # In units of 1e-4
        'eta_cutoff': 0,  # In units of 1e-4
        'tfs': 1,
        'top_a': 0,
        'repetition_penalty': 1.18,
        'repetition_penalty_range': 0.5,
        'top_k': 40,
        'min_length': 0,
        'no_repeat_ngram_size': 0,
        'num_beams': 1,
        'penalty_alpha': 0,
        'length_penalty': 1,
        'early_stopping': False,
        'mirostat_mode': 0,
        'mirostat_tau': 5,
        'mirostat_eta': 0.1,
        'guidance_scale': 1,
        'negative_prompt': '',

        'seed': -1,
        'add_bos_token': True,
        'truncation_length': 2048,
        'ban_eos_token': False,
        'skip_special_tokens': True,
        'stopping_strings': []
    }

    response = requests.post(URI, json=request).json()

    result = response['results'][0]['history']['internal'][-1][1]
    history=response['results'][0]['history']
    # 使用正则表达式找到第一个非\n字符之前的所有字符
    match = re.search(r'^[\n]*', json.dumps(result, indent=4))
    # 如果找到匹配，替换它
    if match:
        result = result[match.end():]

    #print(prompt + result)
    output_text = name+"\nPromopt:\n"+prompt + "\n\nResult:"+result+"\n\n====================================================================================== "
    with open(os.path.join(log_dir, "api_log.txt"), "a", encoding="utf-8") as file:
        file.write(output_text+"\n")
    return result, history
    

if __name__ == '__main__':
    user_input = "Please give me a step-by-step guide on how to plant a tree in my backyard."

    # Basic example
    history = {'internal': [], 'visible': []}

    # "Continue" example. Make sure to set '_continue' to True above
    # arr = [user_input, 'Surely, here is']
    # history = {'internal': [arr], 'visible': [arr]}

    run('test',user_input, history,log_dir='./log/test/')
