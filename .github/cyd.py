import requests
import os
import time


base_url = 'https://api.cydarien.com/api/'

response = requests.post(f'{base_url}users/login/', data={
    'username': os.getenv('CYDERIAN_USERNAME'), 'password': os.getenv('CYDERIAN_PASSWORD')
})
try:
    access = response.json()['access']
except:
    print(f" # UNEXPECTED RESPONSE FROM THE SERVER; EXITING...")
    print(response.json())
    exit(1)

    
headers = {'Authorization': f'Bearer {access}'}

response = requests.get(f'{base_url}users/self', headers=headers)
user_id = response.json()['id']

data = {
    'repo': os.getenv('REPO'),
    'commit': os.getenv('GITHUB_SHA'),
    'project': os.getenv('PROJECT_ID'),
}

print(data)

response = requests.post(f'{base_url}users/{user_id}/projects/get_project_id', data, headers=headers)

print(response.content.decode())

print(data)

response = requests.post(f'{base_url}users/{user_id}/git/', data, headers=headers)

print(response.content.decode())

analysis_id = response.json()['analysis']

while True:
  response = requests.get(f'{base_url}users/{user_id}/analyses/{analysis_id}', headers=headers)
  print("==== response from server ==== ", response)
  data = response.json()
  if data['total_crashes'] > 0:
    response = requests.get(f'{base_url}analyses/{analysis_id}/crashes', headers=headers)
    for crash in response.json():
      print(crash['stackTrace'])
    print('Found crashes visit https://redtest.ca to download crashes.')
    exit(1)
  if data['status'] == 'T':
    exit(0)
  time.sleep(30)

