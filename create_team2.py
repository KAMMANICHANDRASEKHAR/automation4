import os
import sys
import requests
from requests.auth import HTTPBasicAuth

# Fetch sensitive data from environment variables
sitename = os.getenv('SITENAME')
org_id = os.getenv('ORG_ID')
email = os.getenv('EMAIL')
api_token = os.getenv('API_TOKEN')
site_id = os.getenv('SITE_ID')

# Get the display_name from command-line arguments
if len(sys.argv) != 2:
    print("Usage: python create_team.py <display_name>")
    sys.exit(1)

display_name = sys.argv[1]

# Headers for requests
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + api_token
}

# Step 1: Check if team exists via GraphQL
query = '''
query {
  teamSearchV2(first: 100, query: "displayName:\"'{}'\"") {
    edges {
      node {
        displayName
      }
    }
  }
}
'''.format(display_name)

response = requests.post(
    f'https://api.atlassian.com/ex/graphql?site={sitename}',
    headers=headers,
    json={'query': query}
)

# Parse response to check for existing team
if response.status_code == 200:
    existing_teams = [edge['node']['displayName'] for edge in response.json()['data']['teamSearchV2']['edges']]
    if display_name in existing_teams:
        print("Team with the same name already exists. Exiting.")
        sys.exit(0)
else:
    print("Failed to check existing teams.")
    print("Status Code:", response.status_code)
    sys.exit(1)

# Step 2: Create the team if not found
create_url = f'https://{sitename}.atlassian.net/gateway/api/public/teams/v1/org/{org_id}/teams/'
data = {
    "description": "This is an example team description.",
    "displayName": display_name,
    "siteId": site_id,
    "teamType": "OPEN"
}

response = requests.post(
    create_url,
    headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
    auth=HTTPBasicAuth(email, api_token),
    json=data
)

# Check creation response
if response.status_code == 201:
    print("Team created successfully!")
    print("Response:", response.json())
else:
    print("Failed to create team.")
    print("Status Code:", response.status_code)
    print("Response:", response.json())
