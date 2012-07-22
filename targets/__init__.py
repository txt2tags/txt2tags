from config import TARGETS_LIST, USE_I18N, COLOR_DEBUG, BG_LIGHT


################################################################################
# General sharing

CONF = {
    'width': 72,
}


################################################################################
# Target specific sharing

# ASCII Art config
AA_KEYS = 'corner border side bar1 bar2 level2 level3 level4 level5 bullet hhead vhead'.split()
AA_VALUES = '+-|-==-^"-=$'  # do not edit here, please use --chars
AA = dict(zip(AA_KEYS, AA_VALUES))

# ReStructuredText config
# http://docs.python.org/release/2.7/documenting/rest.html#sections
RST_KEYS = 'title level1 level2 level3 level4 level5 bar1 bullet'.split()
RST_VALUES = '#*=-^"--'  # do not edit here, please use --chars
RST = dict(zip(RST_KEYS, RST_VALUES))


################################################################################
# i18n - just use if available

if USE_I18N:
    try:
        import gettext
        # If your locale dir is different, change it here
        cat = gettext.Catalog('txt2tags', localedir='/usr/share/locale/')
        _ = cat.gettext
    except:
        _ = lambda x: x
else:
    _ = lambda x: x


################################################################################
# Targets import

for target in TARGETS_LIST:
    exec('import ' + target)
