import os
import csv
import time
import requests
from colorama import Fore

# Function to get current members of the GitHub organization
def get_org_members(org_name, token):
    url = f"https://api.github.com/orgs/{org_name}/members"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        members = response.json()
        return [member['login'] for member in members]
    else:
        print(Fore.RED + f"\nFailed to get members: {response.json()}" + Fore.RESET)
        return []

# Function to invite users to GitHub organization
def invite_to_github(org_name, token, emails):
    url = f"https://api.github.com/orgs/{org_name}/invitations"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    for email in emails:
        data = {"email": email}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            print(Fore.GREEN + "\nSuccessfully invited " + Fore.MAGENTA + f"{email}\n" + Fore.RESET)
        elif response.status_code == 422:
            print(Fore.MAGENTA + f"\n{email}" + Fore.YELLOW + " is already a member of the organization." + Fore.RESET)
        else:
            print(Fore.RED + f"\nFailed to invite {email}: {response.json()}" + Fore.RESET)

# Main function
def main():
    org_name = "ROFIES-IIITP"
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN is not set in environment variables")

    # Path to the CSV file
    csv_file_path = '../Contact Information ROFIES - Form Responses 1.csv'

    # Read emails from CSV file
    emails = []
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            emails.append(row['Email linked to your GitHub Account'])  # Use the correct column name

    # Get current members of the GitHub organization
    current_members = get_org_members(org_name, token)

    # Invite users to GitHub organization if they are not already members
    emails_to_invite = [email for email in emails if email not in current_members]
    invite_to_github(org_name, token, emails_to_invite)
    
    input(Fore.LIGHTCYAN_EX + "\nPress Enter to exit..." + Fore.RESET)

if __name__ == "__main__":
    main()
