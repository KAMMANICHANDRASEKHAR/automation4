import sys
import requests

# Fetch environment variables
import os
sitename = os.getenv('SITENAME')
org_id = os.getenv('ORG_ID')
email = os.getenv('EMAIL')
api_token = os.getenv('API_TOKEN')
site_id = os.getenv('SITE_ID')  # Ensure SITE_ID is also passed if needed
display_name = sys.argv[1]

# Construct API URL and headers
url = f'https://{sitename}.atlassian.net/gateway/api/public/teams/v1/org/{org_id}/teams/'
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}
auth = (email, api_token)

# Data to send
data = {
    "description": "Team description",
    "displayName": display_name,
    "siteId": site_id,
    "teamType": "OPEN"
}

# Send the API request
response = requests.post(url, headers=headers, auth=auth, json=data)

# Handle response
if response.status_code == 201:
    print("Team created successfully.")
    sys.exit(0)  # Success
elif response.status_code == 409:  # Conflict: team already exists
    print("Team already exists.")
    sys.exit(1)  # Fail the job
else:
    print(f"Failed to create team. Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    sys.exit(1)  # Fail the job for other errors
