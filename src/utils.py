import binascii
from typing import Dict, Union
from pathlib import Path


def pluck(obj: Dict, key_path: str) -> Union[int, str]:
    """Deep query a dictionary"""
    for key in key_path.split('.'):
        obj = obj[key]
    return obj


# is_gz_file is from https://stackoverflow.com/a/54720588
def is_gz_file(filepath: Union[Path, str]) -> bool:
    """
    Test whether file is .gz
    """
    with open(filepath, 'rb') as test_f:
        return binascii.hexlify(test_f.read(2)) == b'1f8b'
