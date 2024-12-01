import os


def get_filepath_input(day_number: str | int) -> str:
    """
    Get the filepath of the file containing input data for a given day.

    Args:
        day_number (str | int):
            The Advent of Code's puzzle's respective day. It should be a
            numeric value between 1 and 25, both included.

    Returns:
        A string containing the filepath of the file containing input data for
        the given day.
    """

    return os.path.join(os.getcwd(), f"day_{day_number:0>2}.txt")
