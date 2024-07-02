import os
from PIL import Image
import requests
from io import BytesIO

# Fetch the GitHub token from the environment variable
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
ORG_NAME = "ROFIES-IIITP"
IMAGE_WIDTH = 800
IMAGE_HEIGHT = 200
AVATAR_SIZE = 100

if not GITHUB_TOKEN:
    print("Error: GITHUB_TOKEN environment variable is not set.")
    exit(1)

# Fetch organization members
response = requests.get(
    f"https://api.github.com/orgs/{ORG_NAME}/members",
    headers={"Authorization": f"token {GITHUB_TOKEN}"}
)

if response.status_code == 200:
    members = response.json()
else:
    print(f"Failed to fetch members. Status code: {response.status_code}")
    print(response.json())
    exit(1)

# Create a blank image
image = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), (255, 255, 255))

# Paste avatars onto the image
x_offset = 0
y_offset = 0
for member in members:
    avatar_url = member["avatar_url"]
    avatar_response = requests.get(avatar_url)
    avatar = Image.open(BytesIO(avatar_response.content))
    avatar = avatar.resize((AVATAR_SIZE, AVATAR_SIZE), Image.LANCZOS)
    image.paste(avatar, (x_offset, y_offset))
    x_offset += AVATAR_SIZE
    if x_offset >= IMAGE_WIDTH:
        x_offset = 0
        y_offset += AVATAR_SIZE

# Save the image
image.save("members.png")
