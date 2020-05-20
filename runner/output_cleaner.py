import logging
from os import listdir, remove
from os.path import isfile, join
from pathlib import Path


logger = logging.getLogger(__file__)


def clean_empty_files_from_folder(path_to_target_folder: str):
    only_files = [
        join(path_to_target_folder, file)
        for file in listdir(path_to_target_folder) if isfile(join(path_to_target_folder, file))
    ]

    empty_files = [file for file in only_files if Path(file).stat().st_size == 0]

    for file in empty_files:
        print(f'deleting empty file: {file}')
        remove(file)
