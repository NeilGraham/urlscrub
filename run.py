import sys, json
from argparse import ArgumentParser

from scrape import scrape_urls

def parse_args(args_list:list[str]):
    parser = ArgumentParser()
    parser.add_argument(
        "--url", required=True, nargs='+',
        help="URL to parse information from." )
    parser.add_argument(
        '--skip_login', action="store_true",
        help="If specified, skips login on websites specified." )
    
    return parser.parse_args(args_list)

def main(args_list:list[str]):
    args = parse_args(args_list)
    res = scrape_urls(args)
    print(json.dumps(res))
    
if __name__ == "__main__":
    main(sys.argv[1:])