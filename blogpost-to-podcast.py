#!/usr/bin/env python
import os
import subprocess
import sys
import tempfile
import urllib

from goose import Goose
import pocket
import soundcloud

if 'POCKET_ACCESS_TOKEN' not in os.environ:
  redirect_uri = 'http://google.com/'
  request_token = pocket.Pocket.get_request_token(consumer_key=os.environ['POCKET_CONSUMER_KEY'], redirect_uri=redirect_uri)
  auth_url = pocket.Pocket.get_auth_url(code=request_token, redirect_uri=redirect_uri)
  raw_input('Go to %s and press enter once approved\n' % auth_url)
  user_credentials = pocket.Pocket.get_credentials(consumer_key=os.environ['POCKET_CONSUMER_KEY'], code=request_token)
  access_token = user_credentials['access_token']
  print 'POCKET_ACCESS_TOKEN=%s' % access_token
  sys.exit(1)

if 'SOUNDCLOUD_ACCESS_TOKEN' not in os.environ:
  redirect_uri = 'http://google.com/'
  client = soundcloud.Client(client_id=os.environ['SOUNDCLOUD_CLIENT_ID'], client_secret=os.environ['SOUNDCLOUD_CLIENT_SECRET'], redirect_uri=redirect_uri)
  code = raw_input('Go to %s and copy the code query string followed by enter once approved\n' % client.authorize_url())
  access_token = client.exchange_token(code).access_token
  print 'SOUNDCLOUD_ACCESS_TOKEN=%s' % access_token
  sys.exit(1)

pocket_instance = pocket.Pocket(os.environ['POCKET_CONSUMER_KEY'], os.environ['POCKET_ACCESS_TOKEN'])
soundcloud_instance = soundcloud.Client(client_id=os.environ['SOUNDCLOUD_CLIENT_ID'], client_secret=os.environ['SOUNDCLOUD_CLIENT_SECRET'], access_token=os.environ['SOUNDCLOUD_ACCESS_TOKEN'])
g = Goose()
for (id, pocket_article) in pocket_instance.get(detail_type='simple')[0]['list'].items():
  url = pocket_article['resolved_url']
  article = g.extract(url=url)

  f = tempfile.NamedTemporaryFile()
  tmpname = '%s.aiff' % f.name
  p = subprocess.Popen(('say', '-o', tmpname), stdin=subprocess.PIPE)
  p.stdin.write(article.cleaned_text.encode('utf-8'))
  p.stdin.close()
  p.wait()

  soundcloud_instance.post('/tracks', track={
    'title': article.title or 'Unnamed article',
    'sharing': 'public',
    'asset_data': open(tmpname)
  })
  os.unlink(tmpname)
  pocket_instance.archive(id).commit()
