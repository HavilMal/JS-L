import argparse

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('--parent', type=int)

print(parser.parse_args().parent)

