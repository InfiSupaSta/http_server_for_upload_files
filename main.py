from http import server
import pathlib
import sys
import os
import logging

from writers.file_writer import FileWriter
from writers.base import Writer

logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO,
                    format='%(message)s')

BASE_DIR = pathlib.Path(__file__).parent
DOWNLOAD_FOLDER_NAME = 'downloads'


class RequestHandler(server.BaseHTTPRequestHandler):
    """
        Class for only one purpose - handle POST requests to download
        upcoming files.
        For curl use cases like example below:

        curl -X POST --upload-file ./dont_touch_me/C_shildt.pdf localhost:8080
    """

    download_folder_name = DOWNLOAD_FOLDER_NAME
    default_request_version = 'HTTP/1.0'

    def set_headers(self):
        self.send_response(200)
        self.send_header('Host', 'localhost')
        self.send_header("Content-Type", "text/html")
        self.send_header('Location', f'{self.path}')
        self.end_headers()

    def do_HEAD(self):
        self.set_headers()

    @staticmethod
    def make_html(message: str):
        html = f"<html><body> <p>{message}</p> </body></html>"
        return html.encode('utf-8')

    def do_GET(self):
        self.wfile.write(
            self.make_html('Hello from simple hTTP server for uploading files via POST request!')
        )

    def do_POST(self):
        self.set_headers()

        filesize = int(
            self.headers.get('content-length', 0)
        )
        filename = os.path.basename(self.path)

        upload_success = self._upload_file(filesize, filename)
        if upload_success:
            self.send_response(200)
            logger.info(f'File {filename} successfully uploaded.')
        else:
            self.send_response(400)
            logger.info(f'File was not provided, wrong HTTP version used or file {filename} already exists.')

    def _upload_file(self, filesize: int, filename: str, writer: Writer = FileWriter()):

        if not pathlib.Path.exists(
                BASE_DIR.joinpath(self.download_folder_name)
        ):
            pathlib.Path(
                BASE_DIR.joinpath(self.download_folder_name)
            ).mkdir()

        absolute_path_to_file = pathlib.Path(self.download_folder_name).joinpath(filename)

        if not all(
                (not pathlib.Path(absolute_path_to_file).exists(), filesize > 0)
        ):
            return False

        file_data = self.rfile.read(filesize)

        with writer as file_writer:
            file_writer.write(self.download_folder_name, filename, file_data, filesize)

        if self._check_file_uploaded_successfully(file_data, absolute_path_to_file):
            return True
        return False

    @staticmethod
    def _check_file_uploaded_successfully(source_file: bytes, destination_file: pathlib.Path):
        with open(destination_file, 'rb') as uploaded_file:
            data = uploaded_file.read()

        if source_file != data:
            return False
        return True


class Server:
    default_server_address = ('localhost', 8080)

    def __init__(self,
                 *,
                 server_address: tuple[str, int] = None,
                 handler_class,
                 ):
        if server_address:
            self.server_address = server_address
        else:
            self.server_address = self.default_server_address
        self.handler = handler_class
        self._server = None

    def start_server(self):
        self._server = server.HTTPServer(server_address=self.server_address,
                                         RequestHandlerClass=self.handler)
        logger.info(f"Server on {self.server_address} start working.")
        return self._server


if __name__ == '__main__':

    if len(sys.argv) > 2:
        from cli_parser.main import command
        command.execute()

    else:
        try:
            srvr = Server(handler_class=RequestHandler).start_server()
            srvr.serve_forever()
        except KeyboardInterrupt:
            logger.info('Server stop working due to keyboard interruption.')
            sys.exit(0)
        except Exception as exc:
            logger.info(f'Server stop working. Reason: {exc}')
