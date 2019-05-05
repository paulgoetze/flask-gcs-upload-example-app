"""Helper functions for testing"""

from io import BytesIO
from os.path import join, dirname, abspath

FIXTURES_DIR = 'fixtures'


def load_file_data(filename: str, path: str = FIXTURES_DIR) -> tuple:
    """ Load and return the data for the given fixture file"""

    return load_binary_file(filename, path), filename


def load_binary_file(filename: str, path: str = FIXTURES_DIR) -> BytesIO:
    """Load and return the given file as binary data"""

    with open(file_path(filename, path), 'rb') as data:
        return BytesIO(data.read())


def file_path(filename: str, path: str = FIXTURES_DIR) -> str:
    """Return the absolute path to the given file"""

    relative_path = join(dirname(__file__), path)
    absolute_path = abspath(relative_path)

    return join(absolute_path, filename)
