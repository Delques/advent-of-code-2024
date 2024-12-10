import inspect
from pathlib import Path

FOLDER_INPUT = "input"
EXTENSION_INPUT = "txt"


def get_filepath_input() -> str:
    """
    Get the filepath of the file containing input data for a given day.
    This expects them to be .txt files named after their respective day
    and positioned in the /input/ folder, e.g.:

        root

        ├── input

        │   ├── day_01.txt

        │   └── day_02.txt

        └── python

            ├── day_01.py

            └── day_02.py

    Returns:
        A string containing the filepath of the file containing input
        data for the given day.
    """

    return Path(
        Path.cwd(),
        FOLDER_INPUT,
        Path(inspect.stack()[1].filename).name[:-2] + EXTENSION_INPUT,
    )
