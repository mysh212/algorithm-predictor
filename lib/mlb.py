from core.general import *

import requests
from bs4 import BeautifulSoup as bs

import pandas as pd

import numpy as np
from numpy import nan, inf

#%%
soup_pre = {}
def get_soup(page):
    if page in soup_pre: return soup_pre[page];
    url = f'https://www.mlb.com/stats/?page={page}'
    html = requests.get(url)
    soup = bs(html.text, 'html.parser')
    soup_pre[page] = soup
    return soup

    # len(html.text)

#%%
def get_columns(soup):
    ans = ([i.find('div').find('abbr').text for i in soup.find('table', class_ = 'bui-table').find('thead').find_all('th')])
    debug(ans)
    return ans

def get_table(soup):
    ans = []
    for i in soup.find('table', class_ = 'bui-table').find('tbody').find_all('tr'):
        user = (i.find('th').find('div').find('a')['aria-label'])
        ans.append([user] + [j.text for j in i.find_all('td')])
    return ans

def get_all_page(soup):
    page = ([int(i.text) for i in soup.find('div', role = 'navigation').find('div').find_all('div')])
    return page

#%%
def main():
    ans = []
    for i in get_all_page(get_soup(1)):
        info(f'Getting page {i}')
        ans = ans + get_table(get_soup(i))

    for i in range(len(ans)):
        for j in range(len(ans[i])):
            try:
                ans[i][j] = int(ans[i][j])
            except:
                try:
                    ans[i][j] = float(ans[i][j])
                except:
                    pass

    df = pd.DataFrame(ans, columns = get_columns(get_soup(1)))
    return df

#%%

if __name__ == '__main__':
    info(main())

# %%
