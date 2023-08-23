### Prints embedding results in a markdown style table
from pathlib import Path
import os
import json
import sys

embeddings = ['TransD', 'TransE', 'TransH', 'RotatE']
WRITE_TO_FILE = False

def get_value_as_percentage(value):
    percentage = value * 100
    formatted_percentage = "{:.2f}%".format(percentage)
    return formatted_percentage

def print_results(write_to_file=WRITE_TO_FILE):
    working_dir = Path(__file__).parent

    if write_to_file is True:
        f = open(
            os.path.join(working_dir, 'results', 'results.md'), 'w') #Write results to results.txt
        sys.stdout = f

    print('<h3>Head Entity Prediction</h3>\n')
    print('|Model   |MR   |hits@10 |hits@3 | hits@1|')
    print('|---|---|---|---|---|')
    for embedding in embeddings:
        json_path = os.path.join(working_dir, 'results', embedding, 'results.json')
        file = open(json_path, 'r')
        file_content = json.load(file)
        mr = file_content['metrics']['head']['optimistic']['arithmetic_mean_rank']
        hits1 = file_content['metrics']['head']['optimistic']['hits_at_1']
        hits3 = file_content['metrics']['head']['optimistic']['hits_at_3']
        hits10 = file_content['metrics']['head']['optimistic']['hits_at_10']
        print(f"|{embedding}   |{mr}   |{get_value_as_percentage(hits10)}   |{get_value_as_percentage(hits3)}   |{get_value_as_percentage(hits1)}   |")

    print('<h3>Tail Entity Prediction</h3>\n')
    print('|Model   |MR   |hits@10 |hits@3 | hits@1|')
    print('|---|---|---|---|---|')
    for embedding in embeddings:
        json_path = os.path.join(working_dir, 'results', embedding, 'results.json')
        file = open(json_path, 'r')
        file_content = json.load(file)
        mr = file_content['metrics']['tail']['optimistic']['arithmetic_mean_rank']
        hits1 = file_content['metrics']['tail']['optimistic']['hits_at_1']
        hits3 = file_content['metrics']['tail']['optimistic']['hits_at_3']
        hits10 = file_content['metrics']['tail']['optimistic']['hits_at_10']
        print(f"|{embedding}   |{mr}   |{get_value_as_percentage(hits10)}   |{get_value_as_percentage(hits3)}   |{get_value_as_percentage(hits1)}   |")

