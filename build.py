# Buildscript for extension
# Packages extension into VSIX using vsce

import os
import json
import semver
import argparse
import requests

# This is the hard-coded branch, change whenever applicable
branch = "-DEV"

parser = argparse.ArgumentParser()
parser.add_argument('action', nargs='?', default='build', choices=['build', 'publish'], help='Action to perform')
parser.add_argument("-b", "--build-only", action="store_true", help="build the extension without bumping patch version")
args = parser.parse_args()

version = "?"

if not args.build_only:
    with open('package.json') as f:
        data = json.load(f)

    version = semver.bump_patch(data['version']) + branch
    data['version'] = version

    with open('package.json', 'w') as f:
        json.dump(data, f, indent=4)
    
os.system("vsce package")
filename = f"frc-devtools-{version}.vsix"

if args.action == "publish":
    owner = 'LDMGamingYT'
    repo = 'FRC-Development-Tools'
    print (f"\nPreparing to create release on {owner}/{repo}\n")

    release_body = input("Release body? (Markdown is supported)\n")
    print('\n')
    with open("GH_TOKEN", 'r') as f:
        token = f.read()

    # Set the required request headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {token}'
    }

    # Construct the release payload
    payload = {
        'tag_name': version,
        'target_commitish': 'HEAD',
        'body': release_body,
        'draft': False,
        'prerelease': False
    }

    print("Sending payload:", payload, '\n')

    # Send the API request to create the release
    response = requests.post(
        f'https://api.github.com/repos/{owner}/{repo}/releases',
        headers=headers,
        data=json.dumps(payload)
    )

    # Check the response status code
    if response.status_code == 201:
        print('Release created successfully.')
    else:
        print(f'Failed to create release. Response: {response.text}')