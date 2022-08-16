# Author     : Hazza3100
# Github     : https://github.com/Hazza3100
# Description: Replit Aio
import os
import string
import random
import time
import pystyle
import requests
import threading

from colorama import Fore, init


init(convert=True)


version = "1"



ver_check = requests.get('https://raw.githubusercontent.com/Hazza3100/ReplitGen/main/Aio/version.txt').text
if version in ver_check:
    #print(f"{Fore.GREEN}Up to date ✅")
    status = "Latest"
else:
    #print(f"{Fore.RED}Outdated ❌")
    status = "Outdated"


init(convert=True)
sem = threading.Semaphore(200)

def get_id(username):

    headers_get_id = {
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

    json_get_id = [
        {
            'operationName': 'ProfilePublicRepls',
            'variables': {
                'username': 'gf',
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

    user_id = requests.post('https://replit.com/graphql', headers=headers_get_id, json=json_get_id).json()[0]['data']['user']['id']
    return user_id


class Follow():

    def follow(username):

        user_id = get_id(username)
        data = open('input/cookies.txt', 'r').read().splitlines()
        cookie = random.choice(data)
        
        headers_follow = {
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


        json_follow = [
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

        r = requests.post('https://replit.com/graphql', headers=headers_follow, json=json_follow)
        print(r.text)
        if r.status_code == 200:
            print(f"{Fore.GREEN}[+] {Fore.RESET}Follow\n")
        else:
            print(f"{Fore.RED}[-] {Fore.RESET}Error\n")

    def unfollow(username):

        user_id = get_id(username)
        data = open('input/cookies.txt', 'r').read().splitlines()
        cookie = random.choice(data)
        
        headers_unfollow = {
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


        json_unfollow = [
            {
                'operationName': 'SetFollowing',
                'variables': {
                    'input': {
                        'targetUserId': user_id,
                        'shouldFollow': False,
                    },
                },
                'query': 'mutation SetFollowing($input: setFollowingInput!) {\n  setFollowing(input: $input) {\n    ... on FollowResult {\n      targetUser {\n        id\n        isFollowedByCurrentUser\n        followerCount\n        __typename\n      }\n      __typename\n    }\n    ... on NotFoundError {\n      __typename\n      message\n    }\n    ... on UnauthorizedError {\n      __typename\n      message\n    }\n    ... on UserError {\n      __typename\n      message\n    }\n    __typename\n  }\n}\n',
            },
        ]

        r = requests.post('https://replit.com/graphql', headers=headers_unfollow, json=json_unfollow)
        print(r.text)
        if r.status_code == 200:
            print(f"{Fore.GREEN}[+] {Fore.RESET}Follow\n")
        else:
            print(f"{Fore.RED}[-] {Fore.RESET}Error\n")




class Extra():

    
    def forker(link):

        cookies = open('cookies.txt', 'r').read().splitlines()
        cookie = random.choice(cookies)

        headers_fork = {
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

        json_fork = [
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

        r = requests.post('https://replit.com/graphql', headers=headers_fork, json=json_fork)
        if r.status_code == 200:
            print(f"{Fore.GREEN}Forked {Fore.RESET}{link}")
        else:
            print("Error")
    
    def run(repl_id):

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

    def report(username, report_reason):

        cookies = open('input/cookies.txt', 'r').read().splitlines()
        cookie = random.choice(cookies)
        
        user_id = get_id(username)


        headers_report = {
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

        json_report = [
            {
                'operationName': 'ReportUser',
                'variables': {
                    'reportedUserId': user_id,
                    'reason': report_reason,
                },
                'query': 'mutation ReportUser($reportedUserId: Int, $reason: String!) {\n  createBoardReport(reportedUserId: $reportedUserId, reason: $reason) {\n    __typename\n    id\n    reportedUser {\n      id\n      __typename\n    }\n  }\n}\n',
            },
        ]

        r = requests.post('https://replit.com/graphql', headers=headers_report, json=json_report)
        if r.status_code == 200:
            print(f"{Fore.GREEN}+{Fore.RESET}\n")
        else:
            print(F"{Fore.RED}Error{Fore.RESET}\n")


    def check_user(string_length):

        with sem:
            proxy = open('input/proxies.txt', 'r').read().splitlines()
            pr = random.choice(proxy)
            proxies = {'http': f'http://{pr}','https':f'http://{pr}'}
            strings = "".join(random.SystemRandom().choice(string.ascii_lowercase)for _ in range(string_length))
            username = strings

            headers = {
                'authority': 'replit.com',
                'accept': 'application/json',
                'accept-language': 'en-GB,en;q=0.9',
                'origin': 'https://replit.com',
                'referer': 'https://replit.com/signup?from=landing',
                'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
            }

            json = {
                'username': username,
            }

            r = requests.post('https://replit.com/data/user/exists', headers=headers, json=json, proxies=proxies)
            if "false" in r.text:
                print(f"{Fore.MAGENTA}Available |{Fore.RESET} {username}")
                open('out/available.txt', 'a').write(f'{username}\n')
            else:
                print(f"{Fore.MAGENTA}Taken |{Fore.RESET} {username}")



def title():
    title = pystyle.Write.Print(f"""
                    ██████╗ ███████╗██████╗ ██╗     ██╗████████╗   █████╗ ██╗ █████╗ 
                    ██╔══██╗██╔════╝██╔══██╗██║     ██║╚══██╔══╝  ██╔══██╗██║██╔══██╗
                    ██████╔╝█████╗  ██████╔╝██║     ██║   ██║     ███████║██║██║  ██║
                    ██╔══██╗██╔══╝  ██╔═══╝ ██║     ██║   ██║     ██╔══██║██║██║  ██║
                    ██║  ██║███████╗██║     ███████╗██║   ██║     ██║  ██║██║╚█████╔╝
                    ╚═╝  ╚═╝╚══════╝╚═╝     ╚══════╝╚═╝   ╚═╝     ╚═╝  ╚═╝╚═╝ ╚════╝ """, pystyle.Colors.blue_to_white, interval=0.0001)
    return title


os.system('cls')
def menu():
    os.system(f'title Replit Aio ^| Made by : github.com/Hazza3100 ^| Status: {status}')
    title()



    print("")
    print("")
    print("")

    print(f'                       {Fore.RED}[{Fore.RESET} {Fore.BLUE}1{Fore.RESET} {Fore.RED}]{Fore.RESET} Follow Bot')
    print(f'                       {Fore.RED}[{Fore.RESET} {Fore.BLUE}2{Fore.RESET} {Fore.RED}]{Fore.RESET} Unfollow Bot')
    print(f'                       {Fore.RED}[{Fore.RESET} {Fore.BLUE}3{Fore.RESET} {Fore.RED}]{Fore.RESET} Fork Bot')
    print(f'                       {Fore.RED}[{Fore.RESET} {Fore.BLUE}4{Fore.RESET} {Fore.RED}]{Fore.RESET} Run Bot')
    print(f'                       {Fore.RED}[{Fore.RESET} {Fore.BLUE}5{Fore.RESET} {Fore.RED}]{Fore.RESET} Report User')
    print(f'                       {Fore.RED}[{Fore.RESET} {Fore.BLUE}6{Fore.RESET} {Fore.RED}]{Fore.RESET} Username Checker')
    print(f'                       {Fore.RED}[{Fore.RESET} {Fore.BLUE}7{Fore.RESET} {Fore.RED}]{Fore.RESET} Credits')


    print("")
    print("")
    print("")


    choice = int(input(f"{Fore.MAGENTA} [{Fore.CYAN}?{Fore.MAGENTA}] Enter Choice {Fore.CYAN}> {Fore.WHITE}"))

    if choice == 1:
        username = input("Enter username > ")
        threads = input("Enter amount of followers > ")
        for i in range(int(threads)):
            threading.Thread(target=Follow.follow, args=(username,)).start()


    if choice == 2:
        username = input("Enter username > ")
        threads = input("Enter amount of followers > ")
        for i in range(int(threads)):
            threading.Thread(target=Follow.unfollow, args=(username,)).start()

    if choice == 3:

        link = input("Enter link to fork > ")
        threads = input("Amount of forks > ")
        for i in range(int(threads)):
            threading.Thread(target=Extra.forker, args=(link,)).start()
    
    if choice == 4:

        repl_id = input("Enter repl id > ")
        threads = input("Amount of runs [Start with 10] > ")
        for i in range(int(threads)):
            threading.Thread(target=Extra.run, args=(repl_id,)).start()
    
    if choice == 5:

        username = input("Enter repl id > ")
        report_reason = input("Enter report reason > ")
        threads = input("Amount of reports > ")
        for i in range(int(threads)):
            threading.Thread(target=Extra.report, args=(username, report_reason,)).start()

    if choice == 6:

        string_length = input("String Length > ")
        threads = input("Amount to Check > ")
        for i in range(int(threads)):
            threading.Thread(target=Extra.check_user, args=(string_length,)).start()

    if choice == 7:
        os.system("cls")
        title()
        print("")
        print(Fore.MAGENTA + f"                                         ╔════════════(Credits)═════════════╗")
        print(Fore.MAGENTA + f"                                         ║ {Fore.CYAN} Made by {Fore.MAGENTA}{Fore.CYAN}github.com/Hazza3100  {Fore.MAGENTA}  ║{Fore.RESET}")
        print(Fore.MAGENTA + f"                                         ╚══════════════════════════════════╝")                                               
        print("")
        print("")
        time.sleep(4)
        input(Fore.MAGENTA + f"            Press any key to continue {Fore.CYAN}> {Fore.WHITE}")
        os.system('cls')
        menu()










os.system('cls')
menu()