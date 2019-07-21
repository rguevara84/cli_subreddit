import argparse
import requests
import os
import praw
import time

oauth_id = os.environ['OAUTH_CLIENT_ID']
oauth_secret = os.environ['OAUTH_SECRET_KEY']
dev_user = os.environ['DEV_USER_ID']
dev_passwd = os.environ['DEV_PASSWORD']
user_agent = "subredditwatcher/0.1 by rguevara"


def create_parser():
    parser = argparse.ArgumentParser(description="""Monitor subreddit post of user
    existing on keybase
    """)
    parser.add_argument('subredditname', help='Subreddit to monitor')
    parser.add_argument('--last', help='Fetch last N messages',
            nargs=1,
            type=int)
    parser.add_argument('--live', help='--live true')
    return parser

reddit = praw.Reddit(client_id=oauth_id, \
                     client_secret=oauth_secret, \
                     user_agent=user_agent, \
                     username=dev_user, \
                     password=dev_passwd)


def keybase_user_check(users):
    """Checks for user on keybase and extract key fingerprint"""
    valid_users = {}
    username = ""
    fingerprint = ""
    headers = {"User-Agent": user_agent}
    payload = {"reddit": users}
    r = requests.get("https://keybase.io/_/api/1.0/user/discover.json", headers=headers, data=payload)
    print(r.status_code)
    matches = r.json()[u'matches'][u'reddit']
    for match in matches:
        for user in match:
            if user != None:
                if user[u'public_key'] != None:
                    fingerprint = user[u'public_key'][u'key_fingerprint']
                    username = user[u'username']
                    valid_users[username] = user[u'public_key'][u'key_fingerprint']
                else:
                    print(username + "Matches but Missing key")
            else:
                username = user[u'username']
                print(username + "Doesn't match")
    return valid_users


def get_messages_last(subbreddit, limit):
    """Fetch activity of a given subreddit"""
    subreddit = reddit.subreddit(subbreddit)
    authors = []
    messagelist = {}
    for message in subreddit.new(limit=limit):
        authors.append(message.author.name)
    userlist = ','.join(set(authors))
    valid_users = keybase_user_check(userlist)
    for messages in subreddit.new(limit=limit):
        if messages.author.name.lower() in valid_users:
            fingerprint = valid_users[messages.author.name.lower()]
            messagelist[messages.id] = {'author' : messages.author.name, \
                                        'fingerprint':fingerprint, \
                                        'title': messages.title }
    return messagelist


def get_post_live(subreddit):
    """Fetch live stream of a given subreddit"""
    authors = []
    messagelist = {}
    print('Connected...\n Fetching messages...\n')
    for message in reddit.subreddit(subreddit).stream.submissions(skip_existing=True):
        print(message.title)
        # Control request rate to keybase
        time.sleep(4)
        valid_user = keybase_user_check(message.author.name)
        if valid_user:
            print(valid_user)
        if message.author.name.lower() in valid_user:
            fingerprint = valid_users[message.author.name.lower()]
            messagelist[message.id] = {'author' : message.author.name, \
                                    'fingerprint':fingerprint, \
                                    'title': message.title }
    return messagelist


def main():
    args = create_parser().parse_args()
    if args.live:
        messages = get_post_live(args.subredditname)
        for message in messages:
            print(messages[message])
    else:
        last = args.last
        messages = get_messages_last(args.subredditname, last[0])
        for message in messages:
            print(messages[message])

main()
