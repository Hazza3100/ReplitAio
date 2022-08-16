import threading
import requests

from colorama import Fore


repl_id = "repl_id"


def run():

    headers_run = {
        'authority': 'replit.com',
        'accept': '*/*',
        'accept-language': 'en-GB,en;q=0.9',
        'cookie': 'replit_ng=1660652900.02.48.973374|8035451343a2d8f3e54599c71b2aec19; connect.sid=s%3AW7_fKvRqEnrGmoC1vxU60kDChoK7MW7Q.K36R1cak9U3HSTXFxV7344AOHJ%2BVWE7wfvFz9Ler%2FUU; gating_id=5c787f2d-4450-4712-ae94-c6c194752516; amplitudeSessionId=1660652898; gating_id=5c787f2d-4450-4712-ae94-c6c194752516; gfa_ref=(not%20provided); gfa_landed_on=/login?goto=%252Frepls; ajs_anonymous_id=5c787f2d-4450-4712-ae94-c6c194752516; _ga=GA1.2.1282159229.1660652898; _gid=GA1.2.1998671421.1660652898; _gat=1; __hstc=205638156.3d4b8b758f9630b4e89a49fa2b546095.1660652898575.1660652898575.1660652898575.1; hubspotutk=3d4b8b758f9630b4e89a49fa2b546095; __hssrc=1; __hssc=205638156.1.1660652898575; ajs_user_id=15903929; replit:authed=1; replit_authed=1; ld_uid=15903929; _dd_s=logs=1&id=04b43705-9666-4b0c-a7e0-650cff244d6c&created=1660652898138&expire=1660653834153&rum=0',
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


for i in range(10):
    threading.Thread(target=run).start()
