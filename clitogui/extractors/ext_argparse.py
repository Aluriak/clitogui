"""Definitions of the function allowing to get from an argparse object
a normalized object.

"""

def argparse_extractor(parser):
    """
    Constructor used by the ExtractedParser object if the used parser
    is argparse.
    """
    subparsers = []
    arguments = []
    # We don't want help actions for now
    parser._actions = [x for x in parser._actions \
                       if not isinstance(x, argparse._HelpAction)]

    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            for parser_name in action.choices:
                list_actions = [i for i in action.choices[parser_name]._actions\
                             if not isinstance(i, argparse._HelpAction)]
                subparser = {}
                subparser["name"] = parser_name
                subparser["list_actions"] = []
                for option in list_actions:
                    subparser["list_actions"].append(argparse_action_normalizer(option))
                subparsers.append(subparser)
        else:
            arguments.append(argparse_action_normalizer(action))
    return subparsers, arguments

def argparse_action_normalizer(action):
    """
    Return representation of given argparse action in the model.
    """
    arg = {}
    if action.option_strings != []:
        arg['cli'] = action.option_strings[0]
    else:
        arg['cli'] = action.option_strings
    arg['name'] = action.dest
    arg['choices'] = action.choices
    arg['help'] = action.help
    arg['default'] = action.default
    if action.type is not None:
        arg['type'] = action.type
    elif isinstance(action, argparse._StoreAction):
        arg['type'] = str
    elif isinstance(action, (argparse._StoreTrueAction, \
                    argparse._StoreConstAction,\
                    argparse._StoreFalseAction)):
        arg['type'] = bool
    elif isinstance(action, argparse._AppendAction):
        arg['type'] = "append_action"
    elif isinstance(action, argparse._CountAction):
        arg['type'] = 'count_action'
    elif isinstance(action, argparse._VersionAction):
        arg['type'] = 'version_action'
    else:
        raise TypeError("Unsupported argument type: ", type(action))
    return arg
