#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

pushd . &>/dev/null

cd $DIR
git checkout 22827be -- hashcrack/static/wordlists/rockyou.txt.xz
rm hashcrack/static/wordlists/rockyou.txt

python setup.py sdist

popd &>/dev/null
