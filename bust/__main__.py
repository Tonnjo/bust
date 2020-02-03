#!/usr/bin/env python3
"""bust register tool

Usage:
  bust.py FILE [-o DIR] [-F | -f] [-u] [-d | -p] [-b] [-t] [-i] [-m] [-a]
  bust.py --version
  bust.py -h | --help

Options:
  -o DIR         Specify output directory. Overrides settings (either JSON dir, or specified project dir in JSON)
  -f             Force overwrite of existing files except module top level VHDL file
  -F             Force overwrite of ALL existing files
  -u             Try to update top-level file - MAY OVERWRITE USER EDITS!
  -d             Do not generate documentation (neither LaTeX nor PDF)
  -p             Do not generate PDF from LaTeX
  -b             Do not generate the bus VHDL package file
  -t             Do not generate the testbench VHDL file and the simulation scripts
  -i             Do not generate the include header files (.h, .hpp & .py)
  -m             Do not generate the module VHDL files
  -a             Update register addresses and save JSON file
  -h --help      HELP!
  --version      Show version info

Arguments:
  FILE         Module configuration file, JSON format
  DIR          Output directory for VHDL, header files and documentation

"""
from docopt import docopt
import sys
import logging

from bust.utils import json_parser
from bust.module import Module
from bust.bus import Bus
from bust.header import Header
from bust.documentation import Documentation
from bust.settings import Settings
from bust.testbench import Testbench
from bust.generation import generate_output
from bust.exceptions import FormatError, InvalidAddress, InvalidRegister, InvalidBusType, InvalidResetMode

__VERSION__ = '0.8.0-dev'


def main():
    args = docopt(__doc__, help=True, version="bust " + __VERSION__)
    logging.basicConfig(filename='debug.log', filemode='w', datefmt='%a, %d %b %Y %H:%M:%S',
                        format='%(asctime)s %(name)-15s %(levelname)-8s %(message)s', level=logging.DEBUG)
    # Define a handler which writes INFO or higher to sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # Define a simpler format for sys.stderr
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logger = logging.getLogger(__name__)

    if args['-a']:
        # TODO
        raise NotImplementedError("The address update feature is not yet implemented")

    try:

        if args['FILE'] is not None:
            json_file = args['FILE']

            logger.info('Parsing file: ' + json_file + '...')

            try:
                json_dict = json_parser(json_file)
                settings = Settings(json_file, json_dict['settings'])
                bus = Bus(json_dict['bus'])
                module = Module(json_dict['module'], bus, settings)
                header = Header(module)
                documentation = Documentation(module)
                testbench = Testbench(module, bus, settings)

            except (FormatError, InvalidAddress, InvalidRegister, InvalidResetMode, InvalidBusType) as e:
                logger.error(str(e))
                exit(1)

            except Exception as e:
                logger.error('\nERROR:\nAn unknown error has occurred...')
                logger.debug(str(e))
                exit(1)

            # File generation settings
            gs = {}

            if args['-o'] is None:
                gs['dir'] = settings.project_path
            else:
                gs['dir'] = args['-o']

            # Check if force overwrite is set
            gs['force_ow'] = False
            gs['force_ow_top'] = False
            if args['-F']:
                gs['force_ow'] = True
                gs['force_ow_top'] = True
            elif args['-f']:
                gs['force_ow'] = True

            # Check if top-level are to be updated
            gs['update_top'] = False
            if args['-u']:
                gs['update_top'] = True
                gs['force_ow_top'] = True

            if bus.bus_type == 'axi':
                gs['gen_bus'] = True
            else:
                gs['gen_bus'] = False
            if args['-b']:
                gs['gen_bus'] = False

            gs['gen_doc'] = True
            gs['gen_pdf'] = True
            if args['-d']:
                gs['gen_doc'] = False
                gs['gen_pdf'] = False
            elif args['-p']:
                gs['gen_pdf'] = False

            gs['gen_tb'] = True
            if args['-t']:
                gs['gen_tb'] = False

            gs['gen_header'] = True
            if args['-i']:
                gs['gen_header'] = False

            gs['gen_mod'] = True
            if args['-m']:
                gs['gen_mod'] = False

            generate_output(settings, bus, module, header, documentation, testbench, gs)

        elif args['-c'] and args['FILE'] is not None:
            raise NotImplementedError("The menu system is removed")

        elif args['-e'] and args['FILE'] is not None:
            raise NotImplementedError("The menu system is removed")

    except Exception:
        logger.exception('An unresolvable error has occurred...')
        exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()