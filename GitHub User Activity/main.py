import requests

while True:
    username = input('Enter username: ')

    response = requests.get(f'https://api.github.com/users/{username}/events')

    if response.status_code != 200:
        print('Invalid username.')
    
    else:
        break

data = response.json()

events_count = {'PullRequestEvent': 0, 'PushEvent': 0, 'IssuesEvent': 0, 'WatchEvent': 0, 'ForkEvent': 0, 'CreateEvent': 0}

for event in data:
    events_count[event['type']] += 1

for event in events_count.keys():
    print(f"No. of {event} is {events_count[event]}")