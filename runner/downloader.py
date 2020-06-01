from typing import Iterator, Tuple

import requests


def spanish_congress_sequential_request_generator(end_of_sequence: int) -> Iterator[Tuple[str, str]]:
    link_to_pdf_pattern = 'http://www.congreso.es/public_oficiales/L14/CONG/DS/PL/DSCD-14-PL-{}.PDF'
    dest_file_name_pattern = 'output/session_{}.pdf'

    for val in range(end_of_sequence):
        yield dest_file_name_pattern.format(val), link_to_pdf_pattern.format(val)


def download_files(targets: Iterator[Tuple[str, str]]):

    for destination_file_path, link_to_target in targets:
        request = requests.get(link_to_target)

        with open(destination_file_path, 'wb') as destination_file:
            destination_file.write(request.content)
