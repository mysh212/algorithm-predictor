"""
GET /problemset HTTP/2
Host: codeforces.com
Sec-Ch-Ua: "Not;A=Brand";v="24", "Chromium";v="128"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Full-Version: ""
Sec-Ch-Ua-Arch: ""
Sec-Ch-Ua-Platform: "Windows"
Sec-Ch-Ua-Platform-Version: ""
Sec-Ch-Ua-Model: ""
Sec-Ch-Ua-Bitness: ""
Sec-Ch-Ua-Full-Version-List: 
Accept-Language: zh-TW,zh;q=0.9
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.120 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://codeforces.com/groups
Accept-Encoding: gzip, deflate, br
Priority: u=0, i
"""

from core.general import *
import requests

def text_to_header(x: str):
    pre = x.split('\n')
    method = pre[0].split()[0].upper()
    url = pre[1].split(': ', 2)[1]
    sub_url = pre[0].split()[1]
    debug([url, sub_url])
    ans = {}
    for i in pre[2:]:
        try:
            if i.startswith('#'): continue;
            ans[i.split(': ',2)[0]] = i.split(': ',2)[1]
        except:
            warning(f'Failed to deal with line {i}, Ignoring.')
    return method, url, sub_url, ans

def repeat(headers: str):
    content = headers.split('\n')[2:]
    method, url, sub_url, ans = text_to_header(headers)
    pre = {'GET': requests.get, 'POST': requests.post}
    debug([url, sub_url, ans])
    return pre[method](f'http://{url}{sub_url}', headers = ans)

def main(x):
    return repeat(x)

if __name__ == '__main__':
    __import__('..core.general').error('You should use this as a module.')
