import argparse
from server import start_server, clear_cache


def main():
    parser = argparse.ArgumentParser(description='A simple CLI program for cache proxy.')
    subparsers = parser.add_subparsers(dest='command')

    start_parser = subparsers.add_parser('start')
    start_parser.add_argument('--port', type=int, required=True)
    start_parser.add_argument('--origin', type=str, required=True)

    clear_parser = subparsers.add_parser('clear-cache')

    args = parser.parse_args()

    if args.command == 'start':
        port = args.port
        origin = args.origin
        start_server(port, origin)
        pass

    if args.command == 'clear-cache':
        clear_cache()

if __name__ == '__main__':
    main()