import random
import threading
import requests

from colorama import Fore


repl_id = input("Enter repl id > ")
repl_link = input("Enter repl link > ")


def like():

    cookies = open('cookies.txt', 'r').read().splitlines()
    cookie = random.choice(cookies)


    headers = {
        'authority': 'replit.com',
        'accept': '*/*',
        'accept-language': 'en-GB,en;q=0.9',
        'cookie': cookie,
        'origin': 'https://replit.com',
        'referer': repl_link,
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    json_data = [
        {
            'operationName': 'LikeButtonToggleReplLike',
            'variables': {
                'input': {
                    'replId': repl_id,
                },
            },
            'query': 'mutation LikeButtonToggleReplLike($input: ToggleReplLikeInput!) {\n  toggleReplLike(input: $input) {\n    ... on Repl {\n      id\n      likeCount\n      currentUserDidLike\n      __typename\n    }\n    __typename\n  }\n}\n',
        },
    ]

    r = requests.post('https://replit.com/graphql', cookies=cookies, headers=headers, json=json_data)
    if r.status_code == 200:
        print(f"{Fore.GREEN}+{Fore.RESET}\n")
    else:
        print(F"{Fore.RED}Error{Fore.RESET}\n")


threads = input("Amount of runs > ")
for i in range(int(threads)):
    threading.Thread(target=like).start()
