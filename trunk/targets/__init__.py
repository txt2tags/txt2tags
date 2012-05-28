from config import TARGETS_LIST

for target in TARGETS_LIST:
    exec('import ' + target)
