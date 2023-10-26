import os, time, requests


base_url = 'https://api.cydarien.com/api'
username = os.getenv('CYDERIAN_USERNAME')
password = os.getenv('CYDERIAN_PASSWORD')

try:
    response = requests.post(f'{base_url}/users/login/', data={
        'username': username, 'password': password
    })
    print(response.json())
    headers = {'Authorization': f'Bearer {response.json()["access"]}'}
except:
    print('#### AUTH FAILED! ####')
    print(response.json())
    exit(1)

response = requests.get(f'{base_url}/users/self', headers=headers)
user_id = response.json()['id']

data = {
    'repo': os.getenv('GITHUB_REPOSITORY'),
    'commit': os.getenv('GITHUB_SHA'),
    'host': 'GitHub',
}

print(data)

response = requests.post(f'{base_url}/users/{user_id}/projects/by_path/', data, headers=headers)

print(response.content.decode())

data['project'] = response.json()['id']

response = requests.post(f'{base_url}/users/{user_id}/git/', data, headers=headers)

print(response.content.decode())

analysis_id = response.json()['analysis']

while True:
  response = requests.get(f'{base_url}/users/{user_id}/analyses/{analysis_id}', headers=headers)
  print("==== response from server ==== ", response)
  data = response.json()
  if data['total_crashes'] > 0:
    response = requests.get(f'{base_url}/analyses/{analysis_id}/crashes', headers=headers)
    for crash in response.json():
      print(crash['stackTrace'])
    print('Found crashes visit https://redtest.ca to download crashes.')
    exit(1)
  if data['status'] == 'T':
    exit(0)
  time.sleep(30)

