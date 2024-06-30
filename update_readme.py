import os
import requests

org_name = os.getenv('ORG_NAME')
token = os.getenv('GITHUB_TOKEN')

headers = {
    'Authorization': f'token {token}'
}

response = requests.get(f'https://api.github.com/orgs/{org_name}/members', headers=headers)
members = response.json()

members_markdown = "<center>\n<div>\n"

for member in members:
    avatar_url = member['avatar_url']
    username = member['login']
    members_markdown += f'<a href="https://github.com/{username}"><img src="{avatar_url}" alt="{username}" width="100" height="100" style="margin: 10px;"></a>\n'

members_markdown += "</div>\n</center>\n"

readme_path = 'README.md'
with open(readme_path, 'r') as file:
    readme_content = file.readlines()

# Find the placeholder in the README where the members will be inserted
start_marker = "<!-- MEMBERS-START -->"
end_marker = "<!-- MEMBERS-END -->"
start_index = None
end_index = None

for i, line in enumerate(readme_content):
    if start_marker in line:
        start_index = i
    elif end_marker in line:
        end_index = i
        break

if start_index is not None and end_index is not None:
    # Replace the content between the markers
    readme_content[start_index + 1:end_index] = [members_markdown]

with open(readme_path, 'w') as file:
    file.writelines(readme_content)
