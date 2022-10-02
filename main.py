import sys
from typing import Any
from commands.arguments import Arguments

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
                "Usage of Freqtrade requires a subcommand to be specified.\n"
                "To have the bot executing trades in live/dry-run modes, "
                "depending on the value of the `dry_run` setting in the config, run Freqtrade "
                "as `freqtrade trade [options...]`.\n"
                "To see the full list of options available, please use "
                "`freqtrade --help` or `freqtrade <command> --help`."
            )
    except Exception as err:
        print('Fatal exception: {0}'.format(err))
    finally:
        sys.exit(return_code)