# Buildscript for extension
# Packages extension into VSIX using vsce

import os
import json
import semver
import argparse
import requests
from colorama import Fore, Back, Style
import base64

# This is the hard-coded branch, change whenever applicable
branch = "-DEV"

# TODO: #10 Make this more object-oriented

parser = argparse.ArgumentParser()
parser.add_argument('action', nargs='?', default='build-only', choices=['build-only', 'publish'], help='action to perform')
parser.add_argument("-n", "--no-bump", action="store_true", help="build the extension without bumping patch version")
args = parser.parse_args()

with open('package.json') as f:
    data = json.load(f)

version = data['version']

if not args.no_bump:
    data['version'] = semver.bump_patch(version) + branch

    with open('package.json', 'w') as f:
        json.dump(data, f, indent=4)
    
os.system("vsce package")
filename = f"frc-devtools-{version}.vsix"

class Publisher:
    def __init__(self, owner, repo, isPreRelease):
        self.owner = owner
        self.repo = repo
        self.prerelease = isPreRelease

    def listRelease(self):
        print("todo lmao")

if args.action == "publish":
    if input("This will create a release from main and publish it immediately, proceed? (Y/n) ") == 'n': exit(0)

    publisher = Publisher("LDMGamingYT", "FRC-Development-Tools", True)

    print (f"\nPreparing to create release on {owner}/{repo}\n")

    release_body = input(f"{Style.BRIGHT}Release body? (Markdown is supported){Style.RESET_ALL}\n")
    print('\n')
    with open("GH_TOKEN", 'r') as f:
        token = f.read()

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {token}'
    }

    tag = 'v' + version
    payload = {
        'name': tag,
        'tag_name': tag,
        'target_commitish': 'main',
        'body': release_body,
        'draft': False,
        'prerelease': prerelease
    }

    print("Sending payload:", payload, '\n')

    response = requests.post(
        f'https://api.github.com/repos/{owner}/{repo}/releases',
        headers=headers,
        data=json.dumps(payload)
    )

    if response.status_code == 201:
        print(f'{Back.GREEN}{Fore.BLACK} DONE {Style.RESET_ALL} Release {tag} created successfully. (https://github.com/{owner}/{repo}/releases/tag/{tag})')
    else:
        print(f"""{Back.RED}{Fore.BLACK} ERROR HTTP {response.status_code} {Style.RESET_ALL} Failed to create release. Response: {response.text} (https://github.com/{owner}/{repo}/releases/tag/{tag})
              
Try:
- Checking if a release already exists with that tag
- Make sure you're connected to the internet
""")
        exit(-1)

    url = f"https://api.github.com/repos/{owner}/{repo}/releases/{tag}/assets"

    print (f"\nAttempting to add {filename} to {tag}")

    with open(filename, 'rb') as file:
        binary_data = file.read()
    binary_data = base64.b64encode(binary_data)
    print(f"\n{Back.GREEN}{Fore.BLACK} OK {Style.RESET_ALL} File encoded successfully\n")

    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/octet-stream',
    }

    params = {
        'name': filename
    }

    response = requests.post(url, headers=headers, params=params, data=binary_data)
    response_json = json.loads(response.text)

    if response.status_code == 201:
        print(f"{Back.GREEN}{Fore.BLACK} DONE {Style.RESET_ALL} Successfully added '{filename}' to release {tag}.")
    else:
        print(f"{Back.RED}{Fore.BLACK} ERROR HTTP {response.status_code} {Style.RESET_ALL} Failed to add '{filename}' to {tag}: {response_json}")
        print(f"\nAutomatically deleting release {tag}, as adding release asset failed\n")

        release_id_response = requests.get(
                f'https://api.github.com/repos/{owner}/{repo}/releases/tags/{tag}',
                headers = {
                    'Authorization': f'Token {token}',
                },  
            )

        response = requests.delete(
            release_id_response.json()['url'],
            headers = {
                'Authorization': f'Token {token}',
            },
            data=json.dumps(payload)
        )

        if response.status_code == 201: # TODO: Fix this to check for all 200 codes, not just 201
            print(f"{Back.GREEN}{Fore.BLACK} DONE {Style.RESET_ALL} Successfully deleted release '{tag}'")
        else:
            print(f"{Back.RED}{Fore.BLACK} ERROR HTTP {response.status_code} {Style.RESET_ALL} Failed to delete release '{tag}'. Delete it manually at https://github.com/{owner}/{repo}/releases/tag/{tag}")