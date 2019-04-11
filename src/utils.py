# from https://stackoverflow.com/a/28225794
import binascii

from typing import Union
from pathlib import Path


def recursive_get(d, *args, default=None) -> str:
    if not args:
        return d
    key, *args = args
    return recursive_get(d.get(key, default), *args, default=default)


# is_gz_file is from https://stackoverflow.com/a/54720588
def is_gz_file(filepath: Union[Path, str]) -> bool:
    """
    Test whether file is .gz
    """
    with open(filepath, 'rb') as test_f:
        return binascii.hexlify(test_f.read(2)) == b'1f8b'
