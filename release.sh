#! /bin/bash

set -exuo pipefail

VERSION="$1"

# Check dependencies.
twine -h > /dev/null

# Check for uncommited changes.
set +e
git diff --quiet && git diff --cached --quiet
retcode=$?
set -e
if [[ $retcode != 0 ]]; then
    echo "There are uncommited changes:"
    git status
    exit 1
fi

git pull

# Check that changelog file is up-to-date.
grep "$VERSION" CHANGELOG.md || (echo "Version $VERSION missing in changelog." && exit 1)

tox

# Bump version.
sed -i -e "s/__version__ = \".*\"/__version__ = \"${VERSION}\"/" txt2tags.py
git commit -am "Update version number to ${VERSION} for release."
git tag "$VERSION"

python3 setup.py sdist bdist_wheel --universal
python3 -m twine upload dist/txt2tags-${VERSION}.tar.gz dist/txt2tags-${VERSION}-py2.py3-none-any.whl

git push
git push --tags
