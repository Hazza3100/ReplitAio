# Author     : Hazza3100
# Github     : https://github.com/Hazza3100
# Description: Replit Fork Bot

import threading
import requests
import random


link = input("Enter link to fork > ")


def forker():

    cookies = open('cookies.txt', 'r').read().splitlines()
    cookie = random.choice(cookies)

    headers = {
        'authority': 'replit.com',
        'accept': '*/*',
        'accept-language': 'en-GB,en;q=0.9',
        'cookie': cookie,
        'origin': 'https://replit.com',
        'referer': link,
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    json = [
        {
            'operationName': 'ForkReplCreateRepl',
            'variables': {
                'input': {
                    'originId': '91df81e9-f59e-41ce-bcaa-3d44aebfc0df',
                    'gitRemoteUrl': '',
                },
            },
            'query': 'mutation ForkReplCreateRepl($input: CreateReplInput!) {\n  createRepl(input: $input) {\n    ... on Repl {\n      id\n      url\n      isPrivate\n      language\n      origin {\n        id\n        isOwner\n        __typename\n      }\n      source {\n        release {\n          id\n          repl {\n            id\n            owner {\n              ... on User {\n                id\n                username\n                __typename\n              }\n              ... on Team {\n                id\n                username\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    ... on UserError {\n      message\n      __typename\n    }\n    __typename\n  }\n}\n',
        },
    ]

    r = requests.post('https://replit.com/graphql', headers=headers, json=json)
    if r.status_code == 200:
        print(f"Forked {link}")
    else:
        print("Error")



threads = input("Amount of forks > ")
for i in range(int(threads)):
    threading.Thread(target=forker)
