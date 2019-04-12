# lifted from https://github.com/apra93/cookiecutter-data-science-pp

import inspect
import logging
from pathlib import Path

import pytest

from src import paths

logger = logging.getLogger(__name__)


def get_objects_in_module(module, cls=None):
    objects = []
    all_objects = inspect.getmembers(module)
    for _, obj in all_objects:
        if cls is not None:
            try:
                if not isinstance(obj, cls):
                    continue
            except TypeError:
                continue
        objects.append(obj)
    return objects


test_dir_paths_and_names = [(
    p, "/".join(p.parts[-2:])) for p in get_objects_in_module(paths, Path)
]


@pytest.mark.parametrize("path, name", test_dir_paths_and_names)
def test_importable_dirs_exist(path, name):
    assert path.exists()
