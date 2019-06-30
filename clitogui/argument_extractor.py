#!/usr/bin/python3
"""
Object used to standardise parser informations.
Supported parser: argparse.
"""

##########
# IMPORT #
##########
try:
    import docopt
except ImportError:
    docopt = None
import argparse
from .extractors import argparse_extractor, docopt_extractor

#########
# CLASS #
#########
class ExtractedParser():
    """
    Contain arguments and subparser list.
    The constructor called depended on the parser used.
    """
    def __init__(self, parser):
        self.parser = parser
        self.arguments = []
        self.list_subparsers = []
        if isinstance(parser, argparse.ArgumentParser):
            self.list_subparsers, self.arguments = argparse_extractor(parser)
        elif docopt is not None and isinstance(parser, docopt.Dict):
            self.list_subparsers, self.arguments = docopt_extractor(parser)
        else:
            raise TypeError("Not supported parser: ", type(parser))
