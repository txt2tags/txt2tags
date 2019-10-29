#! /bin/bash

set -euo pipefail

# Go to repo root.
cd "$(dirname "$0")/../../"

cd samples/module/

ln -sf ../../txt2tags.py txt2tags.py

python module-body.py > /dev/null
python module-full.py > /dev/null
