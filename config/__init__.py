"""
StratoDem Analytics : __init__.py
Principal Author(s) : Eric Linden
Secondary Author(s) :
Description :

Notes :

December 26, 2018
"""


check_global_configure = True
check_configure = True


class ProfileWarning(Warning):
    """Normal ImportWarning is ignored by default
    (and other sub-modules use it)"""
    pass


user = 'NOT_SPECIFIED'
DEBUG = False
debug_token = 'debug-token'
