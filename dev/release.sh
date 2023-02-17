#! /bin/bash

set -exuo pipefail

VERSION="$1"
CHANGES="/tmp/txt2tags-$VERSION-changes"

cd "$(dirname ${0})/../"

# Check dependencies.
hub --version > /dev/null
python3 -m twine -h > /dev/null
tox --version > /dev/null

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

./dev/make-release-notes.py "$VERSION" CHANGELOG.md "$CHANGES"

tox

# Bump version.
sed -i -e "s/__version__ = \".*\"/__version__ = \"${VERSION}\"/" txt2tags.py
git commit -am "Update version number to ${VERSION} for release."
git tag -a "$VERSION" -m "$VERSION"

python3 setup.py sdist bdist_wheel --universal
python3 -m twine upload dist/txt2tags-${VERSION}.tar.gz dist/txt2tags-${VERSION}-py2.py3-none-any.whl

git push
git push origin "$VERSION"  # push new tag

# Add changelog to Github release.
hub release create "$VERSION" --file "$CHANGES"
