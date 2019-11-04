#! /bin/bash

set -euo pipefail

cd $(dirname "$0")

pushd markup
txt2tags markup.t2t
popd

pushd rules
txt2tags rules.t2t
popd

pushd userguide
txt2tags userguide.t2t
popd
