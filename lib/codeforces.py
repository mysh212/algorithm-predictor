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

import pandas as pd
import numpy as np
from numpy import nan, inf


def parse_problem(html: str, raw_problem: dict) -> dict:
    # if not exist('1.html'): write_to_file('1.html', get_real_html('https://codeforces.com/problemset/problem/2047/B'));

    soup = bs(html, 'html.parser')
    pre_problem = soup.find('div', class_ = 'problem-statement').find_all('div')
    pre = {}
    for i in pre_problem:
        nc = i.get('class', [None])[0]
        ans = i.text

        if nc in pre: continue;

        for exclude in 'property-title', 'title', 'section-title':
            now = i.find('div', class_ = exclude)
            if now is not None:
                if ans.find(now.text) != 0:
                    continue
                ans = ans.replace(now.text, '', 1)

        pre[nc] = [ans]

#    for i in pre:
#        debug([i, pre[i]])

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
    # debug(problem)

    try:
        problem['contest'] = raw_problem.get('contestId', None)
        problem['index'] = raw_problem.get('index', None)
        problem['tags'] = raw_problem.get('tags', None)
        problem['rating'] = raw_problem.get('points', None)
    except:
        warning('while adding tags and rating to the problem')

    try:
        now = soup.find(class_ = 'sample-test')
        if now is not None:
            inputs = now.find_all('div', class_ = 'input')
            outputs = now.find_all('div', class_ = 'output')
            if len(inputs) != len(outputs):
                error(f'Input numbers and output numbers does not match on problem {pre.get('title', None)}')
            for k in [inputs, outputs]:
                for j in k:
                    if not len(j.find_all('pre')) == 1:
                        error(f'There are not only one input/output in Problem {pre.get('title', None)}')
            problem['sample-input'] = [i.find('pre').text for i in inputs]
            problem['sample-output'] = [i.find('pre').text for i in outputs]
    except:
        warning('while parsing samples')
    
    try:    
        now = soup.find('th', class_ = 'left')
        if not (now is None or now.find('a') is None):
            now = now.find('a').text
            problem['contest-name'] = now
    except:
        warning('while getting contest name')
        pass
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
        pre.append([i['contestId'], i['index'], get_problem_url(i['contestId'], i['index']), i])
#    pre = pre[1000:]
    p = False

    mkdir('data')
    mkdir('data/html')
    mkdir('data/json')

    htmls = ls('data/html')
    jsons = ls('data/json')

    t = 0
    for i in pre:
        if p == True:
            debug(p)
            warning('Sleeping')
            time.sleep(ri(0,3))
        t = t + 1
        contest, index, url, _ = i
        if f'{contest}{index}' not in htmls:
            info(f'[{t}/{len(pre)}] Getting html for problem {index} in contest {contest} using URL {url}.', end = '\r')
            p = True
#            try:
            write_to_file(f'data/html/{contest}{index}',rp.get_real_html(url))
#            except:
#                error(f'while getting html for problem {contest}{index}')
        else:
            warning(f'File found. Skipping probem {contest}{index}')
            p = False
        if f'{contest}{index}.json' not in jsons:
            try:
                info(f'[{t}/{len(pre)}] Parsing JSON for problem {index} in contest {contest} using URL {url}.', end = '\r')
                write_to_file(f'data/json/{contest}{index}.json', json.dumps(parse_problem(read_from_file(f'data/html/{contest}{index}'), i[3])))
            except:
                error(f'while parsing JSON file for problem {contest}{index}')
        else:
            warning(f'File found. Skipping probem {contest}{index}')

def get_all_problems():
    ans = []
    c = len(ls('data/json'))
    t = 0
    for i in ls('data/json'):
        t = t + 1
        pre = json.loads(read_from_file(f'data/json/{i}'))
        title = pre['title']
        info(f'[{t}/{c}] Parsing problem {title} using JSON file.', end = '\r')
        ans.append(pre)
    return ans


def to_csv(problems: list):
    ans = []
    header = []
    c = len(problems)
    t = 0
    for pre in problems:
        t = t + 1
        title = pre['title']
        info(f'[{t}/{c}] Parsing problem {title} using JSON file.', end = '\r')

        for i in pre:
            if i not in header:
                header.append(i)

        tmp = [nan for i in range(len(header))]
        for i in pre:
            tmp[header.index(i)] = pre[i]

        ans.append(tmp)

    for i in range(len(ans)):
        if len(ans[i]) == len(header):
            break
        while len(ans[i]) != len(header):
            ans[i].append(nan)

    pd.DataFrame(ans, columns = header).to_csv('data/result.csv')
    info('Finish exporting to csv.')
    return

def main():
    auto()
        

# for i in problems:
#     debug(get_problem_url(i['contestId'], i['index']))
