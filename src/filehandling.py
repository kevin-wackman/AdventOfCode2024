from pathlib import Path


def open_data_file_as_lines(data_file):
    path = Path("data/{}".format(data_file))
    lines = []
    with path.open() as f:
        lines = f.readlines()
    return lines