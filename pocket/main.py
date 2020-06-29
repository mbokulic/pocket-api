from pocket import Pocket
import requests
import json
import datetime as dt

_consumer_key = '91573-24e647201671a86e3fafd8d6'

##########################
# authorizing the session
##########################

response = requests.post(
    'https://getpocket.com/v3/oauth/request',
    json={
        'consumer_key': _consumer_key,
        'redirect_uri': 'https://google.com'
    },
    headers={
        'Content-Type': 'application/json',
        'X-Accept': 'application/json'
    }
)
payload = json.loads(response.content.decode())
request_token = payload['code']
auth_url = (
    'https://getpocket.com/auth/authorize?'
    'request_token={}&redirect_uri=https://google.com'
).format(request_token)

# go to this URL
auth_url

####################
# get session token
####################

response = requests.post(
    'https://getpocket.com/v3/oauth/authorize',
    json={
        'consumer_key': _consumer_key,
        'code': request_token
    },
    headers={
        'Content-Type': 'application/json',
        'X-Accept': 'application/json'
    }
)
payload = json.loads(response.content.decode())
access_token = payload['access_token']

#########################
# create Pocket instance
#########################

pocket = Pocket(_consumer_key, access_token)

#########
# "work"
#########

books_pocket = pocket.retrieve(
    tag='book', state='all', sort='newest', detailType='complete')


def tf_time(x):
    return dt.datetime.fromtimestamp(x).date().isoformat()


books = []
for value in books_pocket['list'].values():
    books.append({
        'title': (
            value['resolved_title'] if value['resolved_title'] != ''
            else value['given_title']
        ),
        'url': value['given_url'],
        'time': tf_time(int(value['time_updated'])),
        'excerpt': value['excerpt'],
        'tags': list(value['tags'].keys())
    })


#############################
# deleting books from Pocket
#############################

# - do the actual organizing
#   - clean up: add stuff from Typora and workplace to Pocket
#   - clean up: add stuff from bokmarko+reminders to Pocket
#   - deal with work links separately
#   - markdown for non-links (forget Trello for now)
# - add pocket mail to all emails
