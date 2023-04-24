import argparse

from quant import daily


def main(data_type: str, include_eth: bool, calculate_profit: bool) -> None:
    if data_type == 'daily':
        daily.main(include_eth, calculate_profit)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process command line arguments.')

    parser.add_argument('-t', '--type', choices=['daily'], required=True, help='Choosed zipped data type.')
    parser.add_argument('--include-ETH', action='store_true', help='Include ETH in the result.')
    parser.add_argument('--calculate-profit', action='store_true', help='Include calculated profit in the result.')

    args = parser.parse_args()

    main(args.type, args.include_ETH, args.calculate_profit)
