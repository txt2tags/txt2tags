import os
import shutil
import sys

def setup_paths():
    """Copy txt2tags -> txt2tags.py and make it importable."""
    FILE = os.path.abspath(__file__)
    REPO = os.path.abspath(os.path.join(FILE, '..', '..', '..'))
    TXT2TAGS = os.path.join(REPO, 'txt2tags')
    TXT2TAGS_DEST = os.path.join(REPO, 'txt2tags.py')

    # We need the .py extension for importing the module.
    shutil.copy2(TXT2TAGS, TXT2TAGS_DEST)

    # Enable importing the module.
    sys.path.insert(0, REPO)
