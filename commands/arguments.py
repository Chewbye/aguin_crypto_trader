import argparse
from typing import Any, Dict, Optional

from scripts.download_data import download_data

class Arg:
    # Optional CLI arguments
    def __init__(self, *args, **kwargs):
        self.cli = args
        self.kwargs = kwargs

# List of available command line options
AVAILABLE_CLI_OPTIONS = {
    # Download data
    "pairs_file": Arg(
        '--pairs-file',
        help='File containing a list of pairs to download.',
        metavar='FILE',
    ),
    "days": Arg(
        '--days',
        help='Download data for given number of days.',
        type=int,
        metavar='INT',
    ),
    "timeframes": Arg(
        '-t', '--timeframes',
        help='Specify which tickers to download. Space-separated list. '
        'Default: `1m 5m`.',
        choices=['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h',
                 '6h', '8h', '12h', '1d', '3d', '1w', '2w', '1M', '1y'],
        default=['4h', '1d'],
        nargs='+',
    ),
     "timerange": Arg(
        '--timerange',
        help='Specify what timerange of data to use.',
    ),
    "version": Arg(
        '-V', '--version',
        action='version',
        version=f'%(prog)s {"1.0"}',
    )
}

ARGS_COMMON = ["version"]


ARGS_DOWNLOAD_DATA = ["pairs_file", "days", "timerange", "timeframes"]

class Arguments:
    def __init__(self, args = None) -> None:
        self.args = args
        self._parsed_arg: Optional[argparse.Namespace] = None

    def _build_args(self, optionlist, parser):

        for val in optionlist:
            opt = AVAILABLE_CLI_OPTIONS[val]
            parser.add_argument(*opt.cli, dest=val, **opt.kwargs)

    def get_parsed_arg(self) -> Dict[str, Any]:
        """
        Return the list of arguments
        :return: List[str] List of arguments
        """
        if self._parsed_arg is None:
            self._build_subcommands()
            self._parsed_arg = self._parse_args()

        return vars(self._parsed_arg)

    def _parse_args(self) -> argparse.Namespace:
        """
        Parses given arguments and returns an argparse Namespace instance.
        """
        parsed_arg = self.parser.parse_args(self.args)

        # Workaround issue in argparse with action='append' and default value
        # (see https://bugs.python.org/issue16399)
        # Allow no-config for certain commands (like downloading / plotting)
        # if ('config' in parsed_arg and parsed_arg.config is None):
        #     conf_required = ('command' in parsed_arg and parsed_arg.command in NO_CONF_REQURIED)

        #     if 'user_data_dir' in parsed_arg and parsed_arg.user_data_dir is not None:
        #         user_dir = parsed_arg.user_data_dir
        #     else:
        #         # Default case
        #         user_dir = 'user_data'
        #         # Try loading from "user_data/config.json"
        #     cfgfile = Path(user_dir) / DEFAULT_CONFIG
        #     if cfgfile.is_file():
        #         parsed_arg.config = [str(cfgfile)]
        #     else:
        #         # Else use "config.json".
        #         cfgfile = Path.cwd() / DEFAULT_CONFIG
        #         if cfgfile.is_file() or not conf_required:
        #             parsed_arg.config = [DEFAULT_CONFIG]

        return parsed_arg

    def _build_subcommands(self) -> None:
        self.parser = argparse.ArgumentParser(description='Free, open source crypto trading bot')
        self._build_args(optionlist=['version'], parser=self.parser)

        # Build shared arguments (as group Common Options)
        _common_parser = argparse.ArgumentParser(add_help=False)
        group = _common_parser.add_argument_group("Common arguments")
        self._build_args(optionlist=ARGS_COMMON, parser=group)

        subparsers = self.parser.add_subparsers()

        # # Add download-data subcommand
        download_data_cmd = subparsers.add_parser(
             'download-data',
             help='Download backtesting data.',
             parents=[_common_parser],
        )
        download_data_cmd.set_defaults(func=download_data)
        self._build_args(optionlist=ARGS_DOWNLOAD_DATA, parser=download_data_cmd)


