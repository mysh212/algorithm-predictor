# Author : ysh
# 2024/12/05 Thu 12:12:28
from core.general import *
from lib import repeater as rp
import cloudscraper
import requests
from bs4 import BeautifulSoup as bs
import json
import time
from random import randint as ri


def parse_problem(html: str) -> dict:
    # if not exist('1.html'): write_to_file('1.html', get_real_html('https://codeforces.com/problemset/problem/2047/B'));

    soup = bs(html, 'html.parser')
    pre_problem = soup.find('div', class_ = 'problem-statement').find_all('div')
    pre = {}
    for i in pre_problem:
        now = ''
        if i.get('class', None) == None:
            warning([])
            now = None
        else:
            info(i['class'])
            now = i['class'][0]
        debug(i.text)
        pre[now] = pre.get(now, []) + [i.text]

    for i in pre:
        debug([i, pre[i]])

    mark = {
        'title': 'title',
        'TL': 'time-limit',
        'ML': 'memory-limit',
        'Input': 'input-specification',
        'Output': 'output-specification',
        'Note': 'note',
        'Statement': None
    }
    problem = dict([[i, pre.get(mark[i], [None])[0]] for i in mark])
    debug(problem)
    return problem
    
def get_problemlist():
    url = 'https://codeforces.com/api/problemset.problems?problemsetName'
    return requests.get(url).text

# if not exist('problems.json'): write_to_file('problems.json', get_problemlist())

# problems = json.loads(read_from_file('problems.json'))['result']['problems']

def get_problem_url(contest, index):
    return f'https://codeforces.com/problemset/problem/{contest}/{index}'

def auto():
    if not exist('problems.json.cache'):
        write_to_file('problems.json.cache', get_problemlist())
    
    pre = []
    for i in json.loads(read_from_file('problems.json.cache'))['result']['problems']:
        pre.append([i['contestId'], i['index'], get_problem_url(i['contestId'], i['index'])])
#    pre = pre[1000:]
    p = False
    mkdir('html_result')
    mkdir('json_result')

    htmls = ls('html_result')
    jsons = ls('json_result')

    t = 0
    for i in pre:
        if p == True:
            debug(p)
            warning('Sleeping')
            time.sleep(ri(0,3))
        t = t + 1
        contest, index, url = i
        if f'{contest}{index}' not in htmls:
            info(f'[{t}/{len(pre)}] Getting html for problem {index} in contest {contest} using URL {url}.')
            p = True
#            try:
            write_to_file(f'html_result/{contest}{index}',rp.get_real_html(url))
#            except:
#                error(f'while getting html for problem {contest}{index}')
        else:
            warning(f'File found. Skipping probem {contest}{index}')
        if f'{contest}{index}.json' not in jsons:
            try:
                info('Parsing JSON')
                write_to_file(f'json_result/{contest}{index}.json', json.dumps(parse_problem(read_from_file(f'html_result/{contest}{index}'))))
            except:
                error(f'while parsing JSON file for problem {contest}{index}')
        else:
            warning(f'File found. Skipping probem {contest}{index}')

def main():
    auto()
        

# for i in problems:
#     debug(get_problem_url(i['contestId'], i['index']))
