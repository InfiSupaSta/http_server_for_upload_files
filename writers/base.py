import logging

logger = logging.getLogger(__file__)


class Writer:
    """
        Base class with context-manager behaviour
        for chunk-style uploading file.

        Method .write() must be implemented.
    """

    def __init__(self, chunk_size: int = 4096):
        self.chunk_size = chunk_size

    def read_in_chunks(self, file: bytes, filesize: int):

        current_offset = 0
        is_done = False

        while not is_done:
            start, stop = current_offset, current_offset + self.chunk_size

            if stop > filesize:
                stop = filesize
                is_done = True

            yield file[start:stop]
            current_offset += self.chunk_size

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            logger.error(f'[WRITER ERROR] - - {exc_type} :: {exc_val}')

    def write(self, *args, **kwargs):
        raise NotImplemented
