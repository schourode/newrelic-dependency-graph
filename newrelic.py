import datetime
import getpass
import json
import math
import os

import graphviz
import requests

login_email = input('Email address: ')
login_password = getpass.getpass('NewRelic password: ')

session = requests.Session()

login = session.post('https://login.newrelic.com/login', data={
    'login[email]': login_email,
    'login[password]': login_password,
})
login.raise_for_status()

end = datetime.datetime.now()
start = end - datetime.timedelta(days=7)

request = session.get('https://rpm.newrelic.com/accounts/788482/service_maps/connections.json?' +
    f'end={int(end.timestamp())}&start={int(start.timestamp())}')
request.raise_for_status()

data = request.json()['results'][0]['newCatmap']

paths = dict()

for item in data:
    path_hash = item['nr.pathHash']
    path_details = {
        'context': item['appName'].split('-')[0],
        'is_web': item['transactionType'] == 'Web',
    }
    paths[path_hash] = path_details
    for alt_path_hash in item['nr.alternatePathHashes']:
        paths[alt_path_hash] = path_details

connections = dict()

for item in data:
    if 'nr.referringPathHash' not in item:
        continue
    try:
        from_path = paths[item['nr.referringPathHash']]
        to_path = paths[item['nr.pathHash']]
    except KeyError as e:
        continue # Why does this happen?
    if from_path == to_path:
        continue
    key = (
        from_path['context'],
        to_path['context'],
        from_path['is_web'],
    )
    old_value = connections.get(key, 0)
    connections[key] = old_value + item['callCount']

dot = graphviz.Digraph(engine='dot')
dot.attr('node', shape='box', fontname='Monospace')

max_value = max(connections.values())

for key, value in connections.items():
    dot.edge(
        key[0], key[1],
        penwidth=str(math.ceil(8 * value / max_value)),
        color=('red' if key[2] else 'blue'),
    )

dot.render('./out/graph')
