# CLItoGUI
Python package to generate a GUI from argparse CLI.

Just add the decorator to the main or parser function:

    import clitogui

    @clitogui.on
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

## Used packages:
- pyQt5

## Supported parser:
 - Argparse

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
