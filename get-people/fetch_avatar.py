import requests
import os

# GitHub organization name
org_name = "ROFIES-IIITP"

# GitHub API endpoint to fetch members
api_url = f"https://api.github.com/orgs/{org_name}/members"

# GitHub Personal Access Token (PAT) for authentication
github_token = os.getenv("GITHUB_TOKEN")

if not github_token:
    print("GITHUB_TOKEN environment variable not set. Please set it and try again.")
    exit(1)

# Headers with PAT for authentication
headers = {
    "Authorization": f"token {github_token}"
}

# Fetch members' data from GitHub API
response = requests.get(api_url, headers=headers)

# Check if the response is successful
if response.status_code == 200:
    members = response.json()
    # Save the avatar URLs
    avatar_urls = [member["avatar_url"] for member in members]

    # Save the avatar URLs to a file for further use
    with open("avatar_urls.txt", "w") as file:
        for url in avatar_urls:
            file.write(url + "\n")

    print("Avatar URLs saved to avatar_urls.txt.")
else:
    print(f"Failed to fetch members. Status code: {response.status_code}")
    print(response.text)
