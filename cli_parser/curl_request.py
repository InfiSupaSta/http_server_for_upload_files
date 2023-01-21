import os

from cli_parser.args_storage import ArgsStorage


class CurlRequest:
    template = 'curl -X POST {} --upload-file {} {}:{}'

    def __init__(self):
        self.namespace = ArgsStorage

    def _make_command(self):
        filename = self.namespace.filename
        http_version = f'--http{self.namespace.http_version}' if self.namespace.http_version != '1.0' else ''
        host, port = self.namespace.server_address
        command = self.template.format(http_version, filename, host, port).replace('  ', ' ')
        return command

    def execute(self):
        os.system(self._make_command())
