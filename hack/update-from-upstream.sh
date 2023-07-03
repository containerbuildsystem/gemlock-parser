#!/bin/bash
set -o errexit -o nounset -o pipefail

if [[ ! -e scancode-toolkit ]]; then
    git clone https://github.com/nexB/scancode-toolkit --depth 1 --single-branch
else
    cd scancode-toolkit
    git pull origin develop
    cd ..
fi

cd scancode-toolkit
revision=$(git rev-parse HEAD)
cd ..

python hack/_update_pyfiles.py | while read -r updated_file; do
    sed "s|scancode-toolkit/blob/[a-f0-9]*|scancode-toolkit/blob/$revision|" \
        --in-place "$updated_file"
done

cp -r scancode-toolkit/tests/packagedcode/data/gemfile_lock tests/data/
