import requests
import os

# GitHub organization name
org_name = "ROFIES-IIITP"

# GitHub API endpoint to fetch members
api_url = f"https://api.github.com/orgs/{org_name}/members"

# GitHub Personal Access Token (PAT) for authentication
github_token = os.getenv("GITHUB_TOKEN")

# Headers with PAT for authentication
headers = {
    "Authorization": f"token {github_token}"
}

# Fetch members' data from GitHub API
response = requests.get(api_url, headers=headers)
members = response.json()

# Generate markdown for avatars
avatars_md = "<center>\n<div>\n"
for member in members:
    avatar_url = member["avatar_url"]
    username = member["login"]
    avatars_md += f'<a href="https://github.com/{username}"><img src="{avatar_url}" alt="{username}" width="100" height="100" style="border-radius: 50%; margin: 10px;"></a>\n'
avatars_md += "</div>\n</center>\n"

# Read the README.md content
with open("README.md", "r", encoding="utf-8") as file:
    readme_content = file.read()

# Replace placeholder with avatars markdown
readme_content = readme_content.replace("<!-- MEMBERS-START -->\n<center>\n<div>\n</div>\n</center>\n<!-- MEMBERS-END -->", avatars_md)

# Write updated README.md content
with open("README.md", "w", encoding="utf-8") as file:
    file.write(readme_content)

print("README.md updated with avatars of all members.")
