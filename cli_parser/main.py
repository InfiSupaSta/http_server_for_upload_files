import argparse

from cli_parser.curl_request import CurlRequest, ArgsStorage

parser = argparse.ArgumentParser(description='Process file to upload.')
parser.add_argument('--http',
                    default='1.0',
                    choices=['0.9', '1.0', '1.1'],
                    help='Available HTTP versions.'
                    )
parser.add_argument('--filename',
                    dest='filename',
                    help='Path for file that being uploaded.'
                    )

parsed_args = parser.parse_args(namespace=ArgsStorage)
command = CurlRequest()
