# cli_subreddit
CLI to monitor a subreddit
Depends on: python-pip, pipenv, praw
Steps to install

Clone this repo:

```
git clone git@github.com:rguevara84/cli_subreddit.git
```

cd into dir:

```
cd cli_subreddit
```

* NOTE Make sure to set the following environment variables
* Replace for valid values

```
export OAUTH_CLIENT_ID={reddit_app_client_id}
export OAUTH_SECRET_KEY={}
export DEV_USER_ID={reddi_user}
export DEV_PASSWORD={reddit_password}
```

```
pip install pipenv
```

```
pipenv shell
```

```
make install
```
```
make build
```
```
make install_package
```

usage:
```
eg. with --last setting
redditkeys announcements --last 50

eg. with --live true
redditkeys announcements --live true
```

test without installing package:
```
python src/redditkeys/cli.py announcements --last 200

python src/redditkeys/cli.py announcements --live true
```
