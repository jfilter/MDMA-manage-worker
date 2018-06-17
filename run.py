import json
import secrets

import requests

from scaleway.apis import ComputeAPI

num_open_jobs = requests.get(
    'http://mdma.vis.one/num_open_jobs').json()['num_open_jobs']


api = ComputeAPI(region='ams1', auth_token=secrets.token)

servers = api.query().servers.get()

# find server by name
server_id, server_state = [[x['id'], x['state']]
                           for x in servers['servers'] if x['name'] == 'mdma-worker'][0]

print(server_id)
print(server_state)

if num_open_jobs > 0 and server_state != 'running':
    print(api.query().servers(server_id).action.post({'action': 'poweron'}))

if num_open_jobs == 0 and server_state == 'running':
    print(api.query().servers(server_id).action.post({'action': 'poweroff'}))
