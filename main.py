import sys
from typing import Any
from commands.arguments import Arguments
import logging

if __name__ == '__main__':
    return_code: Any = 1
    try:
        arguments_formatted= sys.argv
        del arguments_formatted[0]
        arguments = Arguments(arguments_formatted)
        args = arguments.get_parsed_arg()


        # Call subcommand.
        if 'func' in args:
            return_code = args['func'](args)
        else:
            # No subcommand was issued.
            raise Exception(
                "A subcommand have to be specified.\n"
            )
    except Exception as err:
        logging.exception('Fatal exception: {0}'.format(err))
    finally:
        sys.exit(return_code)