import sys
import json
from argparse import ArgumentParser

from .scrub import scrub_urls


def parse_args(args_list: list[str]):
    parser = ArgumentParser()

    parser.add_argument(
        "--url", "-l", nargs="+", default=[], help="URL to parse information from."
    )

    parser.add_argument(
        "--search",
        "-s",
        nargs="+",
        default=[],
        help="Search against domain (e.g. 'amazon; Hello world!').",
    )

    parser.add_argument(
        "--driver",
        "-d",
        default="firefox",
        type=str.lower,
        choices=["firefox", "chrome"],
        help="Selenium WebDriver type to use.",
    )

    parser.add_argument(
        "--skip-login",
        action="store_true",
        help="If specified, skips login on websites specified.",
    )

    parser.add_argument(
        "--skip-cookies",
        action="store_true",
        help="If specified, skips adding cookies.",
    )

    parser.add_argument(
        "--db-url",
        default="localhost:3030",
        help="URL connecting to RDF database. "
        "(Defaults to Apache Jena 'localhost:3030')",
    )

    parser.add_argument(
        "--manual-mode",
        action="store_true",
        help="If specified, puts user in an environment where they can manually "
        "enter credentials. Once finished, press enter in the terminal.",
    )

    return parser.parse_args(args_list)


def run(args_list: list[str]=None):
    if args_list is None:
        args_list = sys.argv[1:]
    
    args = parse_args(args_list)

    res = scrub_urls(args)
    
    print(json.dumps(res))
    
    return res
    
    
