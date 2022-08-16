# Author     : Hazza3100
# Github     : https://github.com/Hazza3100
# Description: Replit Follow Bot




import random
import requests
import threading

from colorama import init
from colorama import Fore as color


init(convert=True)


def get_id(username):

    headers = {
        'authority': 'replit.com',
        'accept': '*/*',
        'accept-language': 'en-GB,en;q=0.9',
        'origin': 'https://replit.com',
        'referer': f'https://replit.com/@{username}',
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
            'operationName': 'ProfilePublicRepls',
            'variables': {
                'username': 'Hazza-loltxexfdtx',
                'search': '',
            },
            'query': 'query ProfilePublicRepls($username: String!, $after: String, $search: String) {\n  user: userByUsername(username: $username) {\n    id\n    profileRepls: profileRepls(after: $after, search: $search) {\n      items {\n        id\n        ...ProfilePublicReplsRepl\n        __typename\n      }\n      pageInfo {\n        hasNextPage\n        nextCursor\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ProfilePublicReplsRepl on Repl {\n  id\n  description(plainText: true)\n  isOwner\n  pinnedToProfile\n  timeCreated\n  title\n  url\n  iconUrl\n  ...ReplLinkRepl\n  user {\n    id\n    ...UserLinkUser\n    __typename\n  }\n  templateInfo {\n    label\n    iconUrl\n    __typename\n  }\n  multiplayers {\n    id\n    image\n    username\n    __typename\n  }\n  __typename\n}\n\nfragment ReplLinkRepl on Repl {\n  id\n  url\n  nextPagePathname\n  __typename\n}\n\nfragment UserLinkUser on User {\n  id\n  url\n  username\n  __typename\n}\n',
        },
        {
            'operationName': 'LayoutSiteBanner',
            'variables': {},
            'query': 'query LayoutSiteBanner {\n  siteBanner {\n    id\n    message\n    __typename\n  }\n}\n',
        },
    ]

    user_id = requests.post('https://replit.com/graphql', headers=headers, json=json).json()[0]['data']['user']['id']
    return user_id


class Follow():



    def follow(username):

        user_id = get_id(username)
        data = open('input/cookies.txt', 'r').read().splitlines()
        cookie = random.choice(data)
        
        headers = {
            'authority': 'replit.com',
            'accept': '*/*',
            'accept-language': 'en-GB,en;q=0.9',
            'cookie': cookie,
            'origin': 'https://replit.com',
            'referer': f'https://replit.com/@{username}',
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
                'operationName': 'SetFollowing',
                'variables': {
                    'input': {
                        'targetUserId': user_id,
                        'shouldFollow': True,
                    },
                },
                'query': 'mutation SetFollowing($input: setFollowingInput!) {\n  setFollowing(input: $input) {\n    ... on FollowResult {\n      targetUser {\n        id\n        isFollowedByCurrentUser\n        followerCount\n        __typename\n      }\n      __typename\n    }\n    ... on NotFoundError {\n      __typename\n      message\n    }\n    ... on UnauthorizedError {\n      __typename\n      message\n    }\n    ... on UserError {\n      __typename\n      message\n    }\n    __typename\n  }\n}\n',
            },
        ]

        r = requests.post('https://replit.com/graphql', headers=headers, json=json)
        print(r.text)
        if r.status_code == 200:
            print(f"{color.GREEN}[+] {color.RESET}Follow\n")
        else:
            print(f"{color.RED}[-] {color.RESET}Error\n")




username = input("Enter username > ")
threads = input("Enter amount of followers > ")
for i in range(int(threads)):
    threading.Thread(target=Follow.follow, args=(username,)).start()
