import json
import logging
import os
from string import Template
from typing import List

import tiktoken
import webvtt
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # take environment variables from .env.


CONFIG_FILE = 'model_config.json'
BASE_FILE = 'data/Haystack Europe 2024/Haystack EU 2024 - Aswath N Srinivasan：Leveraging User Behavior Insights to Enhance Search Relevance [0chun264PRQ]'
TRANSCRIPT_FILE = f'{BASE_FILE}.en.vtt'
DESCRIPTION_FILE = f'{BASE_FILE}.description'
CLEAN_FILE = f'{BASE_FILE}.txt'
TEMPLATE_FILE = 'prompts/raw_to_cleaner.txt'


def remove_duplicate_lines_from_captions(vtt_file: str) -> list[str]:
    captions = webvtt.read(vtt_file)

    all_cleaned_lines = []

    for caption in captions:
        lines = caption.text.splitlines()

        # Process lines and avoid duplicates
        for line in lines:
            if not all_cleaned_lines or line != all_cleaned_lines[-1]:
                all_cleaned_lines.append(line)

    return all_cleaned_lines


def fill_template(template_file: str, description_file: str, transcript_lines: List[str]) -> str:
    with open(template_file, 'r') as template_f:
        template_content = template_f.read()

    with open(description_file, 'r') as desc_f:
        description_content = desc_f.read()

    transcript_content = "\n".join(transcript_lines)

    template = Template(template_content)

    filled_template = template.substitute(
        description=description_content,
        transcript=transcript_content
    )

    return filled_template


def count_tokens(input_text: str, model_name: str = 'gpt-4o') -> int:
    tokenizer = tiktoken.encoding_for_model(model_name)
    tokens = tokenizer.encode(input_text)
    return len(tokens)


def call_openai(input_text: str, config_file: str = CONFIG_FILE) -> str:
    with open(config_file, 'r') as config_f:
        config = json.load(config_f)

    client = OpenAI(
        organization='org-D7V3FaxRttvMRF7O7oJ8p3PS',
        project='proj_j6pNSNbTultG8mTTjjq6pjsQ',
    )

    completion = client.chat.completions.create(
        model=config['model_id'],
        messages=[
            {
                "role": "user",
                "content": json.dumps(input_text)
            }
        ]
    )

    return completion.choices[0].message.content


def list_data_files(root_dir: str) -> List[str]:
    valid_file_bases = []

    for subdir, _, files in os.walk(root_dir):
        # Create a set of file bases for easier matching
        file_bases = {os.path.splitext(file)[0] for file in files}

        for base in file_bases:
            if f"{base}.en.vtt" in files and f"{base}.description" in files:
                valid_file_bases.append(os.path.join(subdir, base))

    return valid_file_bases


def main(template_file: str, description_file: str, transcript_file: str) -> str:
    lines = remove_duplicate_lines_from_captions(transcript_file)
    filled_prompt = fill_template(template_file, description_file, lines)
    token_estimate = count_tokens(filled_prompt)
    logging.info(f'Number of input tokens: {token_estimate}')
    clean_text = call_openai(filled_prompt)
    with open(CLEAN_FILE, 'wt') as f:
        f.write(clean_text)
    return clean_text


if __name__ == '__main__':
    main(TEMPLATE_FILE, DESCRIPTION_FILE, TRANSCRIPT_FILE)
