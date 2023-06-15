import requests
from google.cloud import dns

credentials_path = '../key.json'
client = dns.client.Client.from_service_account_json(credentials_path)

project_id = 'devops-project-387209'
zone_name = 'flight-app-zone'

zone = client.zone(project_id, zone_name)

name_servers = zone.name_servers
print(f"Name servers for zone '{zone_name}':")
for name_server in name_servers:
    print(name_server)

key = 'gHf757dnLyaQ_XuLdaiAvVeFk9Sm916QmkC'
secret = '5Xk5yK5LxBaiPXauULHRMh'

headers = {
    "Authorization": f"sso-key {key}:{secret}",
    "Content-Type": "application/json"
}

# Fetch domains
url = "https://api.godaddy.com/v1/domains"
response = requests.get(url, headers=headers)
if response.status_code == 200:
    domains = response.json()
    for domain in domains:
        print(domain['nameServers'])
