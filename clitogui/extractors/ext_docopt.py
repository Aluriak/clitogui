"""Definitions of the function allowing to get from the docopt interface
a group of normalized objects.

"""

import docopt


def docopt_extractor(parsed):
    print('DOCOPT WILL BE HANDLED…')
    print(':', parsed)
    print(':', dir(parsed))
    docopt.old_LeafPattern = LeafPattern
    docopt.LeafPattern = LeakingLeafPattern
    print()
    return [], []


class LeakingLeafPattern(docopt.LeafPattern):
    """Substitute of docopt.LeafPattern that will be replaced before calling docopt"""

    def flat(self):
        ret = super().flat()
        print('\o/ \o/ code successfully injected: flat will return:', ret)
        return ret
