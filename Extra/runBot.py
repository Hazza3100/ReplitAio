import threading
import requests
import random

from colorama import Fore


repl_id = "repl_id"


def run():

    cookies = open('cookies.txt', 'r').read().splitlines()
    cookie = random.choice(cookies)

    headers_run = {
        'authority': 'replit.com',
        'accept': '*/*',
        'accept-language': 'en-GB,en;q=0.9',
        'cookie': cookie,
        'origin': 'https://replit.com',
        'referer': 'https://replit.com/@Hazza-loltxexfdtx/ExperiencedVigorousDemos?v=1',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    json_run = [
        {
            'operationName': 'UserReplViewCreateReplRun',
            'variables': {
                'replId': repl_id,
            },
            'query': 'mutation UserReplViewCreateReplRun($replId: String!) {\n  createReplRun(replId: $replId) {\n    ... on Repl {\n      id\n      runCount\n      __typename\n    }\n    __typename\n  }\n}\n',
        },
    ]

    r = requests.post('https://replit.com/graphql', headers=headers_run, json=json_run)
    if r.status_code == 200:
        print(f"{Fore.GREEN}+{Fore.RESET}\n")
    else:
        print(F"{Fore.RED}Error{Fore.RESET}\n")


threads = input("Amount of views > ")
for i in range(int(threads)):
    threading.Thread(target=run).start()
