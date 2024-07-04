import requests
import os
from PIL import Image
from io import BytesIO

# GitHub organization name
org_name = "ROFIES-IIITP"
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
    exit(1)

# Create a composite image of avatars
IMAGE_WIDTH = 800
IMAGE_HEIGHT = 200
AVATAR_SIZE = 100

# Create a blank image
image = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), (255, 255, 255))

# Paste avatars onto the image
x_offset = 0
y_offset = 0
for avatar_url in avatar_urls:
    avatar_response = requests.get(avatar_url)
    avatar = Image.open(BytesIO(avatar_response.content))
    avatar = avatar.resize((AVATAR_SIZE, AVATAR_SIZE), Image.LANCZOS)
    image.paste(avatar, (x_offset, y_offset))
    x_offset += AVATAR_SIZE
    if x_offset >= IMAGE_WIDTH:
        x_offset = 0
        y_offset += AVATAR_SIZE
    if y_offset >= IMAGE_HEIGHT:
        break  # Stop if the image height limit is reached

# Save the image
image.save("members.png")
print("Composite image of avatars saved as members.png.")
