# Buildscript for extension
# Packages extension into VSIX using vsce

import os
import json
import semver
import argparse

# This is the hard-coded branch, change whenever applicable
branch = "-DEV"

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--build-only", action="store_true", help="build the extension without bumping patch version")
args = parser.parse_args()

if not args.build_only:
    with open('package.json') as f:
        data = json.load(f)

    data['version'] = semver.bump_patch(data['version']) + branch

    with open('package.json', 'w') as f:
        json.dump(data, f, indent=4)
    
os.system("vsce package")