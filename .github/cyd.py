import os, time, requests


api_url = 'https://api.cydarien.com/api'
username = os.getenv('CYDERIAN_USERNAME')
password = os.getenv('CYDERIAN_PASSWORD')
host = os.getenv('REPOSITORY_HOST')
repo = os.getenv('REPOSITORY_PATH')
commit = os.getenv('COMMIT_SHA')
headers = {}
project_id = None

def authenticate():
    global headers
    response = requests.post(f'{api_url}/users/login/', data={
        'username': username, 'password': password
    })
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        print('############  AUTHENTICATION FAILED!  ############')
        print(response.json()['detail'])
        print('##################################################')
        exit(1)
    headers = {'Authorization': f'Bearer {response.json()["access"]}'}

def get_project_id():
    global project_id
    response = requests.post(f'{api_url}/users/self/projects/by_path/',
        headers=headers,
        data={
            'host': host,
            'repo': repo,
        })
    if response.status_code != 200:
        print(response.json()['detail'])
        exit(1)
    project_id = response.json()['id']


if __name__ == "__main__":
    authenticate()
    get_project_id()
    print(project_id)
