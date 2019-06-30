# CLItoGUI
Python package to generate a GUI from argparse CLI, prompting user
about the parameters, allowing him to run the program without
using the command line arguments directly.

Just add the decorator to the main or parser function:

    from clitogui import clitogui

    @clitogui
    def create_parser() -> argparse.ArgumentParser:
        """
        Function to define the parser
        """
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument('square', help="Display a square of a given number",\
                            type=int)
        parser.add_argument('-v', '--verbose', help="Increase output verbosity",\
                            action="store_true")
        parser.add_argument('-i','--iteration', type=int, choices=[0, 1, 2],\
                            help="Iterations number")
        return parser


## Interactive mode
Using the `clitogui.interactive()` decorator, it is possible to get,
instead of a just-at-start GUI that will collapse once the OK button is clicked,
a GUI that will preview the results before printing them.

    import clitogui

    def compute_value(args:argparse.ArgumentParser) -> object:
        return ...  # int, str, PIL.Image,…

    @clitogui.interactive(compute_value, tabulate=True, autorun=False)
    def create_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description=__doc__)
        ...
        return parser

    args = create_parser.parse_args()
    assert args._output == compute_value(args)  # last result is already available

See the [dedicated example](examples/interactive-gui.py) for a better overview.


## Used packages:
- pyQt5

## Supported parser:
- [Argparse](https://docs.python.org/dev/library/argparse.html)
- [docopt](http://docopt.org)

### docopt support limit
Docopt enables very flexible constructions, such as (taken from official example):

      naval_fate.py ship <name> move <x> <y> [--speed=<kn>]

Because of the positional argument between two subparsers,
such an interface cannot be perfectly emulated by argparse, that can achieve these non-perfect solutions:

      naval_fate.py ship move <name> <x> <y> [--speed=<kn>]
      naval_fate.py ship <name> <move> <x> <y> [--speed=<kn>]

In the first reproduction, all subparsers are moved on the first places.
In the second one, an argument `<move>` is added, allowing the user to choose between 1 value: `move`.

In order to keep the code simple and readable, the first solution has been selected.
If you ever want to use that code to bridge accurately the docopt API,
you will need to adapt that part, and it may be quite complex to handle this kind of CLI:

      naval_fate.py ship <name> move <x> <y> [--speed=<kn>]
      naval_fate.py ship <idx>  shift <x> [--speed=<kn>]


### Argparse
See [examples/argparse_full_example.py](examples/argparse_full_example.py) for an example of supported features of argparse.

Note that Argparse [custom types](https://docs.python.org/3/library/argparse.html#type) are supported, using type annotations:

    import clitogui

    @clitogui.clitogui
    def create_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser()
        parser.add_argument('infile', type=existant_file)
        return parser

    def existant_file(filepath:str):  # note the type annotation here
        if not os.path.exists(filepath):
            raise argparse.ArgumentTypeError("file {} doesn't exists".format(filepath))
        return filepath

The type annotation will be used to decide the GUI elements to show.

## Supported GUI:
- PyQt

## TODO List before bêta:
- Add one simple test of cli parsing to Model
- Define Model in its own module
- Use of Model for [argument_extractor](clitogui/argument_extractor.py)
- Support for Tkinter (add `Environment :: X11 Applications :: GTK`)
- Support for docopt

## How does it work?:
TODO
