COMPLEX = """Naval Fate, with a GUI.

Usage:
  naval_fate.py ship new <name>...
  naval_fate.py ship <name> move <x> <y> [--speed=<kn>]
  naval_fate.py ship shoot <x> <y>
  naval_fate.py mine (set|remove) <x> <y> [--moored | --drifting]
  naval_fate.py (-h | --help)
  naval_fate.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --speed=<kn>  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.

"""
BIGGER = """Naval Fate, with a GUI.

Usage:
  naval_fate.py ship new <name>...
  naval_fate.py ship <name> move <x> <y> [--speed=<kn>]

Options:
  -h --help     Show this screen.
  --version     Show version.
  --speed=<kn>  Speed in knots [default: 10].

"""

SIMPLER = """Naval Fate, with a GUI.

Usage:
  naval_fate.py ship new <name>...
  naval_fate.py ship shoot <x> <y>
  naval_fate.py --version

Options:
  --moored      Moored (anchored) mine.

"""
TINYER = """Naval Fate, with a GUI.

Usage:
  naval_fate.py ship new <name>...
  naval_fate.py --version

"""

# import clitogui
import docopt



def docoptwrapper(func:docopt.docopt):
    print('DOCOPT WILL BE HANDLED…')
    assert func is docopt.docopt, func
    print(':', docopt)
    # print(':', dir(docopt))
    # print(':', dir(docopt.Option))

    def my_parse_pattern(source, options):
        import re
        tokens = docopt.TokenStream(re.sub(r'([\[\]\(\)\|]|\.\.\.)', r' \1 ', source), docopt.DocoptLanguageError)
        result = docopt.parse_expr(tokens, options)
        if tokens.current() is not None:
            raise tokens.error('unexpected ending: %r' % ' '.join(tokens))
        my_parse_pattern.docopt_parsed_data = docopt.Required(*result)
        return my_parse_pattern.docopt_parsed_data

    # docopt.old_parse_argv = docopt.parse_argv

    from functools import wraps
    @wraps(func)
    def wrapped_func(doc, argv=None, help=True, version=None, options_first=False):  # taken from docopt source code
        # inject our code
        docopt.old_parse_pattern = docopt.parse_pattern
        docopt.parse_pattern = my_parse_pattern
        try:
            func(doc, argv, help, version, options_first)
        except SystemExit:
            pass ; print("we don't negociate with terrorists")
        # put the correct parse_pattern in place
        docopt.parse_pattern = docopt.old_parse_pattern
        #
        parser = docopt_parsed_value_to_argparse(my_parse_pattern.docopt_parsed_data, version=version)
        return parser
    return wrapped_func


import argparse
def docopt_parsed_value_to_argparse(parsed:docopt, version=None) -> argparse.ArgumentParser:
    print('DOCOPT PARSED:', parsed)
    # print(dir(parsed))
    # print('CHILD:', parsed.children)
    # print('EITHIER:', parsed.either)
    # for child in parsed.children:
        # print('\n', child)
    subparsers = {} # parser -> generator of subparsers
    def get_subparsers(parser:argparse.ArgumentParser, *args, **kwargs) -> argparse.ArgumentParser:
        if parser not in subparsers:
            subparsers[parser] = parser.add_subparsers(*args, **kwargs)
        return subparsers[parser]

    argparser = argparse.ArgumentParser()
    if version:  argparser.add_argument('--version', action='version', version=version)
    make_argparse_tree(parsed, argparser, None)
    return argparser
    # current_subparser = None
    # target_parser = argparser
    # for subparser_name, args, kwargs in make_argparse_arg(parsed, parser_name=None, optional=False):
        # print('>', current_subparser, '.add_argument:', args, kwargs)
        # if subparser_name is None:
            # target_parser.add_argument(*args, **kwargs)
        # else:  # this is a command to create a subparser
            # target_parser = current_subparser = get_subparsers(target_parser).add_parser(subparser_name, *args, **kwargs)
    # return argparser

def make_argparse_object(docobj, optional:bool, **supargs):
    """Yield args/kwargs for ArgumentParser.add_argument"""
    if type(docobj) is docopt.Option:
        if (docobj.long == '--help' and docobj.short == '-h') or docobj.long == '--version':
            # already have been added if necessary
            return None, None
        print()
        print('OPTION:', docobj)
        print()
        if 'debug':
            for field, value in docobj.__dict__.items():
                if field.startswith('_'):  continue
                print(f"\t{field} = '{value}' (type: {type(value)})")
        names = ', '.join([name for name in (docobj.long, docobj.short) if name])
        kwargs = {'default': docobj.value, 'required': not optional, **supargs}
        if optional:  del kwargs['required']  # useless, may only create problems
        return (names,), kwargs
    elif type(docobj) is docopt.Argument:
        name = docobj.name
        if name.startswith('<'): name = name[1:]
        if name.endswith('>'): name = name[:-1]
        return (name,), {'default': docobj.value, **supargs}
    elif type(docobj) is docopt.OneOrMore:
        if len(docobj.children) == 1:
            child = docobj.children[0]
            print('ONE OR MORE:', child)
            if type(child) in {docopt.Argument, docopt.Option}:
                metavar = child.name.upper()  # more descriptive than just 'N'
                return make_argparse_object(child, optional, **{'metavar': metavar, 'nargs': '+'})
            else:
                raise NotImplementedError(f"OneOrMore object contain one child of type {type(child)}: {child}")
        else:
            raise NotImplementedError(f"OneOrMore object contain {len(docobj.children)} children, instead of one: {docobj}")
    else:
        print()
        print(docobj)
        print(dir(docobj))
        raise NotImplementedError(f"Docopt object {docobj} of type {type(docobj)} is not convertible into argparse object")


parser_by_name = {} # (parent parser, parser name) -> parser object
subparsers = {} # parser object -> generator of subparsers
def get_subparsers(parser:argparse.ArgumentParser, *args, **kwargs) -> argparse.ArgumentParser:
    if parser not in subparsers:
        subparsers[parser] = parser.add_subparsers(*args, **kwargs)
    return subparsers[parser]

def make_argparse_sequence(sequence:list or tuple, parser:argparse.ArgumentParser, parser_name:str, parent_parser:argparse.ArgumentParser=None, optional:bool=False):


    current_parser_level = parser
    current_parser_name = parser_name
    print("Parsing a sequence:", type(sequence))
    print("\t", current_parser_name, current_parser_level.prog)
    print("\t", len(sequence), 'objects in sequence')


    # first, go over the Command, and only the Command.
    if any(type(obj) is docopt.Command for obj in sequence):
        # SEE README FOR THAT PROBLEM
        # reorder Command to get them at the beginning of the 

    for obj in sequence:
        print('\t\tObj:', type(obj))
        if type(obj) is docopt.Command:  # update the current parser level
            if (current_parser_level, obj.name) in parser_by_name:
                print('ALREADY ADDED SUBPARSER:', obj.name, '(son of', current_parser_level.prog, ')')
                parent_parser, current_parser_level = current_parser_level, parser_by_name[current_parser_level, obj.name]
                current_parser_name = obj.name
            else:
                print('NEW SUBPARSER:', obj.name, '(son of', current_parser_level.prog, ')')
                new_parser = get_subparsers(current_parser_level, dest=obj.name).add_parser(obj.name)
                parser_by_name[current_parser_level, obj.name] = new_parser
                parent_parser, current_parser_level = current_parser_level, new_parser
                current_parser_name = obj.name
        elif type(obj) is docopt.Argument:
            args, kwargs = make_argparse_object(obj, optional)
            current_parser_level.add_argument(*args, **kwargs)
        elif type(obj) is docopt.Optional:  # update the current parser level
            make_argparse_tree(obj, current_parser_level, current_parser_name, parent_parser, optional=True)
        elif type(obj) is docopt.Option:  # send it back to tree
            make_argparse_tree(obj, current_parser_level, current_parser_name, parent_parser, optional)
        elif type(obj) is docopt.Either:  # send it back to tree
            make_argparse_tree(obj, current_parser_level, current_parser_name, parent_parser, optional)
        elif type(obj) is docopt.Required:  # send it back to self as a tuple
            make_argparse_sequence(obj.children, current_parser_level, current_parser_name, parent_parser, optional=False)
        elif type(obj) is docopt.OneOrMore:  # send it back to self as a tuple
            args, kwargs = make_argparse_object(obj, optional)
            print('ARGS:', args, kwargs)
            current_parser_level.add_argument(*args, **kwargs)
        else:
            raise NotImplementedError(f"Docopt object of type {type(obj)} is not treatable as a sequence")


def make_argparse_tree(docobj:docopt.Required, parser:argparse.ArgumentParser, parser_name:str, parent_parser:argparse.ArgumentParser=None, optional:bool=False):
    print("Parsing a tree:", type(docobj))
    print("\tcurrent parser:", parser.prog)
    print("\tparser_by_name:", len(parser_by_name), {(p.prog, name): parser.prog for (p, name), parser in parser_by_name.items()})
    print("\tsubparsers:", len(subparsers))
    # helpers
    def contains_only_options(either:docopt.Either) -> bool:
        return all(type(child) is docopt.Option for child in either.children)
    def contains_only_commands(either:docopt.Either) -> bool:
        return all(type(child) is docopt.Command for child in either.children)
    def contains_only_required(either:docopt.Either) -> bool:
        return all(type(child) is docopt.Required for child in either.children)

    if type(docobj) is docopt.Required:
        # a coherent suit of things: already implemented in next elif
        make_argparse_tree(docobj.children, parser, parser_name, parent_parser, optional)
    elif isinstance(docobj, (list, tuple)):
        # a coherent suit of things
        make_argparse_sequence(docobj, parser, parser_name, parent_parser, optional)

    elif type(docobj) is docopt.Either:
        if contains_only_options(docobj):  # mutually exclusive options
            group = parser.add_mutually_exclusive_group()
            for child in docobj.children:
                args, kwargs = make_argparse_object(child, optional=True)
                if args is None and kwargs is None: continue
                group.add_argument(*args, **kwargs)
        elif contains_only_commands(docobj):  # mutually exclusive commands
            for child in docobj.children:
                make_argparse_sequence([child], parser, parser_name, parent_parser, optional)
        elif contains_only_required(docobj):
            for child in docobj.children:
                make_argparse_tree(child, parser, parser_name, parent_parser, optional)
        else:
            raise ValueError(f"The Either() node contains unexpected objects: " + repr(docobj.children))
    elif type(docobj) is docopt.Command:
        get_subparsers(parser, dest=docobj.name).add_parser(docopt.name)
    elif type(docobj) is docopt.Optional:
        print('OPTIONAL IS:', docobj)
        assert len(docobj.children) == 1, docobj
        make_argparse_tree(docobj.children[0], parser, parser_name, parent_parser, optional)
    elif type(docobj) is docopt.Option:
        args, kwargs = make_argparse_object(docobj, optional)
        if args is None and kwargs is None: return
        parser.add_argument(*args, **kwargs)
    else:
        print()
        print(docobj)
        print(dir(docobj))
        raise NotImplementedError(f"Docopt object {docobj} of type {type(docobj)} is not treatable as a tree")



if __name__ == '__main__':
    parser = docoptwrapper(docopt.docopt)(BIGGER, version='Naval Fate 2.0')
    print('PARSER:', parser)
    print()
    print('CASE1:', parser.parse_args(['ship', '-h']))
    print()
    print('# CASE2:')
    args = parser.parse_args(['ship', 'new', 'HMS1'])
    print('ARGS:', args)
    print(dir(args))
