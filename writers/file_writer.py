import pathlib

from writers.base import Writer


class FileWriter(Writer):

    def write(self, download_folder, filename: str, file_object, filesize):
        path_to_save = pathlib.Path(download_folder).joinpath(filename)
        with open(path_to_save, 'wb') as file:
            for chunk in self.read_in_chunks(file_object, filesize):
                file.write(chunk)
