from targets_config import TARGETS_LIST

for target in TARGETS_LIST:
    exec('import ' + target)
