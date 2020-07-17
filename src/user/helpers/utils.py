"""common util functions for the user app."""
from uuid import uuid4


def read_file(file_name: str, format: str = 'rb') -> bytes:
    """Read a file, by default, binary file.

    Parameters
    ----------
    file_name : str
        The filename of the file to read, with its exact path.

    format : str
        The file type to read, default binary.

    Returns
    -------
    bytes
        data read from the file
    """
    with open(file=file_name, mode=format) as f:
        data = f.read()
    return data


def make_unique_uuid4_code() -> str:
    """Create a unique UUID4 code.

    Returns
    -------
    str
        A `uuid.uuid4().hex` code.
    """
    return uuid4().hex
