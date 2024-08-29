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

# Other details
description = 'This is an example team description.'
team_type = 'OPEN'

# Construct the URL
url = f'https://{sitename}.atlassian.net/gateway/api/public/teams/v1/org/{org_id}/teams/'

# Headers for the request
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

# Data payload
data = {
    "description": description,
    "displayName": display_name,
    "siteId": site_id,
    "teamType": team_type
}

# Make the POST request to create the team
response = requests.post(
    url,
    headers=headers,
    auth=HTTPBasicAuth(email, api_token),
    json=data
)

# Print the response
if response.status_code == 201:
    print("Team created successfully!")
    print("Response:", response.json())
else:
    print("Failed to create team.")
    print("Status Code:", response.status_code)
    print("Response:", response.json())
