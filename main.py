# Author     : Hazza3100
# Github     : https://github.com/Hazza3100
# Description: Replit Aio
import os
import re
import time
import json
import base64
import string
import random
import pystyle
import requests
import threading


from PyMailGw import MailGwApi
from colorama import Fore, init
from os.path import isfile, join
from capmonster_python import HCaptchaTask


init(convert=True)


version = "1"



ver_check = requests.get('https://raw.githubusercontent.com/Hazza3100/ReplitAio/main/version.txt').text
if version in ver_check:
    #print(f"{Fore.GREEN}Up to date ✅")
    status = "Latest"
else:
    #print(f"{Fore.RED}Outdated ❌")
    status = "Outdated"


init(convert=True)
sem = threading.Semaphore(200)


class config():
    with open('input/settings.json') as f:
        cfg = json.load(f)

    capmonster_key = cfg['Generator']['capmonster_key']
    random_bio = cfg['Generator']['random_bio']
    use_proxy = cfg['Generator']['use_proxy']



class stats():

    genned = 0
    updated = 0
    errors = 0



# Gen


api = MailGwApi(proxy=None, timeout=30)
def get_inbox():

    while True:
        time.sleep(5)
        for mail in api.fetch_inbox():
            content = api.get_message_content(mail['id'])
            s = content
            pat = r":\s+(\S+)"
            res = re.findall(pat, s)
            verify_link = res[1]
        return verify_link






class Generator():


    def gen():
        try:
            proxy = open('input/proxies.txt', 'r').read().splitlines()
            proxy1 = random.choice(proxy)
            proxies = {'http': f'http://{proxy1}','https':f'http://{proxy1}'}

            email = api.get_mail()
            #username = "".join(random.choices(string.ascii_letters + string.digits, k=9))
            us_data = open('input/usernames.txt', 'r').read().splitlines()
            user = random.choice(us_data)
            username = user + "".join(random.choices(string.ascii_letters + string.digits, k=3))
            password = "".join(random.choices(string.ascii_letters + string.digits, k=7)) + "H8_"

            print(f"{Fore.YELLOW} Solving captcha...{Fore.RESET}\n")
            capmonster = HCaptchaTask(config.capmonster_key)
            task_id = capmonster.create_task("https://replit.com/signup", "a20d9b66-6747-404a-9393-c449c4611661")
            result = capmonster.join_task_result(task_id)
            hcaptcha_token = result.get("gRecaptchaResponse")
            print(f"{Fore.LIGHTBLUE_EX} Captcha Solved...{Fore.RESET}\n")



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
                'email': email,
                'username': username,
                'password': password,
                'teacher': False,
                'organization': '',
                'hCaptchaResponse': hcaptcha_token,
                'hCaptchaSiteKey': 'a20d9b66-6747-404a-9393-c449c4611661',
                'source': 'explicit',
            }
            if config.use_proxy == True:
                r = requests.post('https://replit.com/signup', headers=headers, json=json, proxies=proxies)
            if config.use_proxy == False:
                r = requests.post('https://replit.com/signup', headers=headers, json=json)
            stats.genned += 1
            cookies = r.headers['set-cookie']
            s_cookie = cookies.split(';')[4]
            cookie = s_cookie.split(', ')[1]
            print(f"{Fore.GREEN} [+] Generated{Fore.RESET} ({stats.genned})\n")
            open('out/cookies.txt', 'a').write(f'{cookie}\n')
            open('out/accounts.txt', 'a').write(f'{email}:{password}\n')

            pictures = [f for f in os.listdir("avatars/") if isfile(join("avatars/", f))]
            random_pic = random.choice(pictures)

            with open(f'avatars/{random_pic}', "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())


            headers_get_id = {
                'authority': 'replit.com',
                'accept': 'application/json',
                'accept-language': 'en-GB,en;q=0.9',
                'cookie': cookie,
                'origin': 'https://replit.com',
                'referer': 'https://replit.com/account',
                'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
            }

            json_get_id = {
                'image': f"data:image/png;base64,{(encoded_string.decode('utf-8'))}",
                'context': 'profile-image',
            }

            r = requests.post('https://replit.com/data/images/upload', headers=headers_get_id, json=json_get_id) # get upload id
            _id = r.json()['id']


            headers_change = {
                'authority': 'replit.com',
                'accept': '*/*',
                'accept-language': 'en-GB,en;q=0.9',
                'cookie': cookie,
                'origin': 'https://replit.com',
                'referer': 'https://replit.com/account',
                'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
            }

            json_change = [
                {
                    'operationName': 'AccountProfileCurrentUserUpdate',
                    'variables': {
                        'input': {
                            'profileImageId': _id,
                        },
                    },
                    'query': 'mutation AccountProfileCurrentUserUpdate($input: UpdateCurrentUserInput!) {\n  updateCurrentUser(input: $input) {\n    id\n    ...AccountProfileCurrentUser\n    __typename\n  }\n}\n\nfragment AccountProfileCurrentUser on CurrentUser {\n  id\n  username\n  canUpdateUsername: canUpdate(column: USERNAME)\n  firstName\n  lastName\n  bio\n  hasPrivacyRole\n  hasProfileImage\n  image\n  isSubscribed\n  url\n  __typename\n}\n',
                },
            ]

            r1 = requests.post('https://replit.com/graphql', headers=headers_change, json=json_change)

            headers_bio = {
                'authority': 'replit.com',
                'accept': '*/*',
                'accept-language': 'en-GB,en;q=0.9',
                'cookie': cookie,
                'origin': 'https://replit.com',
                'referer': 'https://replit.com/account',
                'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
                }

            random_bios = ['I like to code', 'I know a little bit of python', 'I know a little bit of js', 'I prefer not to use JavaScript', 'Normally I just watch youtube lol']

            if config.random_bio == True:
                bio = random.choice(random_bios)
            if config.random_bio == False:
                bios = open('input/bios.txt', 'r').read().splitlines()
                bio = random.choice(bios)


            r = requests.get('http://names.drycodes.com/10')
            name = r.json()[0]
            first_name = name.split('_')[0]
            last_name = name.split('_')[1]


            json_bio = [
                {
                    'operationName': 'AccountProfileCurrentUserUpdate',
                    'variables': {
                        'input': {
                            'firstName': first_name,
                            'lastName': last_name,
                            'bio': bio,
                        },
                    },
                    'query': 'mutation AccountProfileCurrentUserUpdate($input: UpdateCurrentUserInput!) {\n  updateCurrentUser(input: $input) {\n    id\n    ...AccountProfileCurrentUser\n    __typename\n  }\n}\n\nfragment AccountProfileCurrentUser on CurrentUser {\n  id\n  username\n  canUpdateUsername: canUpdate(column: USERNAME)\n  firstName\n  lastName\n  bio\n  hasPrivacyRole\n  hasProfileImage\n  image\n  isSubscribed\n  url\n  __typename\n}\n',
                },
            ]

            r = requests.post('https://replit.com/graphql', headers=headers_bio, json=json_bio)

            headers_verify = {
                'authority': 'replit.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-language': 'en-GB,en;q=0.9',
                'cookie': cookie,
                'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'service-worker-navigation-preload': 'true',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            }

            r = requests.get(get_inbox(), headers=headers_verify)

            headers_create = {
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


            title = ['My First repl', 'New Project', 'I am starting over', 'I will begin here', 'Probs never gonna finish this', 'How is this?']
            random_title = random.choice(title)

            json_create = [
                {
                    'operationName': 'CreateReplForm2CreateRepl',
                    'variables': {
                        'input': {
                            'title': random_title,
                            'folderId': None,
                            'isPrivate': False,
                            'originId': '8d4142a6-b4ad-4e1c-940b-15b99773aa04',
                            'replReleaseId': 'bfc596de-af6e-4f9e-b0c0-d3747cb8ddef',
                        },
                        'isTitleAutoGenerated': False,
                    },
                    'query': 'mutation CreateReplForm2CreateRepl($input: CreateReplInput!, $isTitleAutoGenerated: Boolean!) {\n  createRepl(input: $input, isTitleAutoGenerated: $isTitleAutoGenerated) {\n    ... on Repl {\n      ...CreateReplForm2Repl\n      __typename\n    }\n    ... on UserError {\n      message\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment CreateReplForm2Repl on Repl {\n  id\n  ...TemplateSelector2Repl\n  __typename\n}\n\nfragment TemplateSelector2Repl on Repl {\n  id\n  url\n  title\n  iconUrl\n  templateLabel\n  nixedLanguage\n  isPrivate\n  isRenamed\n  language\n  likeCount\n  description(plainText: true)\n  deployment {\n    id\n    activeRelease {\n      id\n      __typename\n    }\n    __typename\n  }\n  owner {\n    ... on User {\n      id\n      username\n      __typename\n    }\n    ... on Team {\n      id\n      username\n      __typename\n    }\n    __typename\n  }\n  ...TemplateReplCardRepl\n  __typename\n}\n\nfragment TemplateReplCardRepl on Repl {\n  id\n  iconUrl\n  templateCategory\n  title\n  description(plainText: true)\n  publicReleasesForkCount\n  templateLabel\n  likeCount\n  url\n  owner {\n    ... on User {\n      id\n      ...TemplateReplCardFooterUser\n      __typename\n    }\n    ... on Team {\n      id\n      ...TemplateReplCardFooterTeam\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment TemplateReplCardFooterUser on User {\n  id\n  username\n  image\n  url\n  __typename\n}\n\nfragment TemplateReplCardFooterTeam on Team {\n  id\n  username\n  image\n  url\n  __typename\n}\n',
                },
            ]

            r = requests.post('https://replit.com/graphql', headers=headers_create, json=json_create)

            headers_online = {
                'authority': 'replit.com',
                'accept': '*/*',
                'accept-language': 'en-GB,en;q=0.9',
                'cookie': 'connect.sid=s%3A7zOeFa5vO0BTdxt40pymu6f5OfVmpeLG.IxMF8ZzLjgMTvCn8NEZLSO%2B7TwVwq54ZXnr5DJ7M5mA',
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

            json_online = [
                {
                    'operationName': 'UpdateUserPrivacyPreferences',
                    'variables': {
                        'input': {
                            'show_presence': 'when_online',
                        },
                    },
                    'query': 'mutation UpdateUserPrivacyPreferences($input: UpdateUserPrivacyPreferencesInput!) {\n  updateUserPrivacyPreferences(input: $input) {\n    __typename\n    ... on CurrentUser {\n      id\n      showPresence\n      __typename\n    }\n    ... on UserError {\n      message\n      __typename\n    }\n    ... on UnauthorizedError {\n      message\n      __typename\n    }\n  }\n}\n',
                },
            ]

            r = requests.post('https://replit.com/graphql', headers=headers_online, json=json_online)
            stats.updated += 1
            print(f"{Fore.GREEN}[+] Updated Accounts{Fore.RESET}\n")
        except:
            pass













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
    
    def run(repl_id, link):

        cookies = open('cookies.txt', 'r').read().splitlines()
        cookie = random.choice(cookies)

        headers_run = {
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

    def banner_change():

        cookies = open('input/cookies.txt', 'r').read().splitlines()
        cookie = random.choice(cookies)


        banners = [f for f in os.listdir("banners/") if isfile(join("banners/", f))]
        random_banner = random.choice(banners)

        with open(f'banners/{random_banner}', "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

        headers_id = {
            'authority': 'replit.com',
            'accept': 'application/json',
            'accept-language': 'en-GB,en;q=0.9',
            'cookie': cookie,
            'origin': 'https://replit.com',
            'referer': 'https://replit.com/@account',
            'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        json_id = {
            'image': f"data:image/png;base64,{(encoded_string.decode('utf-8'))}",
            'context': 'profile-cover-image',
        }

        r = requests.post('https://replit.com/data/images/upload', headers=headers_id, json=json_id)
        upload_id = r.json()['id']


        headers_up = {
            'authority': 'replit.com',
            'accept': '*/*',
            'accept-language': 'en-GB,en;q=0.9',
            'cookie': cookie,
            'origin': 'https://replit.com',
            'referer': 'https://replit.com/account',
            'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        json_up = [
            {
                'operationName': 'CoverImageUpdate',
                'variables': {
                    'input': {
                        'imageId': upload_id,
                        'offsetY': 0,
                    },
                },
                'query': 'mutation CoverImageUpdate($input: SetUserCoverImageInput!) {\n  setUserCoverImage(input: $input) {\n    ... on CurrentUser {\n      id\n      ...CoverImageCurrentUser\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment CoverImageCurrentUser on CurrentUser {\n  id\n  coverImage {\n    url\n    offsetY\n    __typename\n  }\n  __typename\n}\n',
            },
        ]

        r = requests.post('https://replit.com/graphql', headers=headers_up, json=json_up)
        if r.status_code == 200:
            print(f"{Fore.GREEN} Updated{Fore.RESET}")
        else:
            print(f"{Fore.RED} Error{Fore.RESET}")


    def pfp_change():

        cookies = open('input/cookies.txt', 'r').read().splitlines()
        cookie = random.choice(cookies)

        pictures = [f for f in os.listdir("avatars/") if isfile(join("avatars/", f))]
        random_pic = random.choice(pictures)

        with open(f'avatars/{random_pic}', "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())


        headers_get_id = {
            'authority': 'replit.com',
            'accept': 'application/json',
            'accept-language': 'en-GB,en;q=0.9',
            'cookie': cookie,
            'origin': 'https://replit.com',
            'referer': 'https://replit.com/account',
            'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        json_get_id = {
            'image': f"data:image/png;base64,{(encoded_string.decode('utf-8'))}",
            'context': 'profile-image',
        }

        r = requests.post('https://replit.com/data/images/upload', headers=headers_get_id, json=json_get_id)
        _id = r.json()['id']


        headers_pfp = {
            'authority': 'replit.com',
            'accept': '*/*',
            'accept-language': 'en-GB,en;q=0.9',
            'cookie': cookie,
            'origin': 'https://replit.com',
            'referer': 'https://replit.com/account',
            'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        json_pfp = [
            {
                'operationName': 'AccountProfileCurrentUserUpdate',
                'variables': {
                    'input': {
                        'profileImageId': _id,
                    },
                },
                'query': 'mutation AccountProfileCurrentUserUpdate($input: UpdateCurrentUserInput!) {\n  updateCurrentUser(input: $input) {\n    id\n    ...AccountProfileCurrentUser\n    __typename\n  }\n}\n\nfragment AccountProfileCurrentUser on CurrentUser {\n  id\n  username\n  canUpdateUsername: canUpdate(column: USERNAME)\n  firstName\n  lastName\n  bio\n  hasPrivacyRole\n  hasProfileImage\n  image\n  isSubscribed\n  url\n  __typename\n}\n',
            },
        ]

        r1 = requests.post('https://replit.com/graphql', headers=headers_pfp, json=json_pfp)
        if r1.status_code == 200:
            print(f"{Fore.GREEN} Updated{Fore.RESET}")
        else:
            print(f"{Fore.RED} Error{Fore.RESET}")

    def bio_change(bio):

        cookies = open('input/cookies.txt', 'r').read().splitlines()
        cookie = random.choice(cookies)

        headers_bio = {
                'authority': 'replit.com',
                'accept': '*/*',
                'accept-language': 'en-GB,en;q=0.9',
                'cookie': cookie,
                'origin': 'https://replit.com',
                'referer': 'https://replit.com/account',
                'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
                }


        json_bio = [
            {
                'operationName': 'AccountProfileCurrentUserUpdate',
                'variables': {
                    'input': {
                        'firstName': "",
                        'lastName': "",
                        'bio': bio,
                    },
                },
                'query': 'mutation AccountProfileCurrentUserUpdate($input: UpdateCurrentUserInput!) {\n  updateCurrentUser(input: $input) {\n    id\n    ...AccountProfileCurrentUser\n    __typename\n  }\n}\n\nfragment AccountProfileCurrentUser on CurrentUser {\n  id\n  username\n  canUpdateUsername: canUpdate(column: USERNAME)\n  firstName\n  lastName\n  bio\n  hasPrivacyRole\n  hasProfileImage\n  image\n  isSubscribed\n  url\n  __typename\n}\n',
            },
        ]

        r = requests.post('https://replit.com/graphql', headers=headers_bio, json=json_bio)
        if r.status_code == 200:
            print(f"{Fore.GREEN} Updated{Fore.RESET}")
        else:
            print(f"{Fore.RED} Error{Fore.RESET}")














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
    os.system(f'title Replit Aio ^| Made by : github.com/Hazza3100 ^| Version: {status}')
    title()



    print("")
    print("")
    print("")


    print(f'                       {Fore.RED}[{Fore.RESET} {Fore.BLUE}0{Fore.RESET} {Fore.RED}]{Fore.RESET} Account Generator')
    print(f'                       {Fore.RED}[{Fore.RESET} {Fore.BLUE}1{Fore.RESET} {Fore.RED}]{Fore.RESET} Follow Bot')
    print(f'                       {Fore.RED}[{Fore.RESET} {Fore.BLUE}2{Fore.RESET} {Fore.RED}]{Fore.RESET} Unfollow Bot')
    print(f'                       {Fore.RED}[{Fore.RESET} {Fore.BLUE}3{Fore.RESET} {Fore.RED}]{Fore.RESET} Fork Bot')
    print(f'                       {Fore.RED}[{Fore.RESET} {Fore.BLUE}4{Fore.RESET} {Fore.RED}]{Fore.RESET} Run Bot')
    print(f'                       {Fore.RED}[{Fore.RESET} {Fore.BLUE}5{Fore.RESET} {Fore.RED}]{Fore.RESET} Report User')
    print(f'                       {Fore.RED}[{Fore.RESET} {Fore.BLUE}6{Fore.RESET} {Fore.RED}]{Fore.RESET} Username Checker')
    print(f'                       {Fore.RED}[{Fore.RESET} {Fore.BLUE}7{Fore.RESET} {Fore.RED}]{Fore.RESET} Banner Changer')
    print(f'                       {Fore.RED}[{Fore.RESET} {Fore.BLUE}8{Fore.RESET} {Fore.RED}]{Fore.RESET} Pfp Changer')
    print(f'                       {Fore.RED}[{Fore.RESET} {Fore.BLUE}8{Fore.RESET} {Fore.RED}]{Fore.RESET} Bio Changer')
    print(f'                       {Fore.RED}[{Fore.RESET} {Fore.BLUE}10{Fore.RESET} {Fore.RED}]{Fore.RESET} Credits')


    print("")
    print("")
    print("")


    choice = int(input(f"{Fore.MAGENTA} [{Fore.CYAN}?{Fore.MAGENTA}] Enter Choice {Fore.CYAN}> {Fore.WHITE}"))

    if choice == 0:
        threads = input("Enter amount of threads > ")
        for i in range(int(threads)):
            threading.Thread(target=Generator.gen).start()

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
        repl_id = input("Enter repl link > ")
        threads = input("Amount of runs [Start with 10] > ")
        for i in range(int(threads)):
            threading.Thread(target=Extra.run, args=(repl_id, link,)).start()
    
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
        threads = input("Amount to change > ")
        for i in range(int(threads)):
            threading.Thread(target=Extra.banner_change).start()

    if choice == 8:
        threads = input("Amount to change > ")
        for i in range(int(threads)):
            threading.Thread(target=Extra.pfp_change).start()
    
    if choice == 9:
        bio = input("Bio to change > ")
        threads = input("Amount to change > ")
        for i in range(int(threads)):
            threading.Thread(target=Extra.bio_change, args=(bio,)).start()


    if choice == 10:
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
