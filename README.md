# blogpost-to-podcast

Fetch your bookmarked posts in pocket, turn them into audio and upload to soundcloud

# Requirements

## OS X

It uses OS X's `say` command to turn the text into audio.

## Tokens

Read from environment variables. Use `daemontools`'s `envdir` to avoid
contaminating your usual environment.

Since the app is serverless, I use google.com as domain for oauth redirect.

* `POCKET_CONSUMER_KEY`: Get it from https://getpocket.com/developer/apps/
* `POCKET_ACCESS_TOKEN`: Once `POCKET_CONSUMER_KEY` is set,
run `blogpost-to-podcast.py` and it will prompt you to authorize the app and
return the environment
* `SOUNDCLOUD_CLIENT_ID`: Get it from http://soundcloud.com/you/apps
* `SOUNDCLOUD_CLIENT_SECRET`: Get it from http://soundcloud.com/you/apps
* `SOUNDCLOUD_ACCESS_TOKEN`: Once `SOUNDCLOUD_CLIENT_ID` and `SOUNDCLOUD_CLIENT_SECRET`
are set, run `blogpost-to-podcast.py`, authorize the app, copy the code from
the querystring and then set the env variable.

## Python

```
pip install -r requirements.txt
```
