import re


def natural_sort(list: list, key: str = "code") -> list:
    """
    Applies a natural sort order to dictionaries inside a given list

    See https://stackoverflow.com/a/8940266

    :param list: list List of dictionaries to be sorted
    :param key: Key to sort by
    :return: list Sorted list
    """

    def get_alphanum_key_func(key):
        convert = lambda text: int(text) if text.isdigit() else text
        return lambda s: [convert(c) for c in re.split("([0-9]+)", key(s))]

    sort_key = get_alphanum_key_func(lambda x: x[key])
    list.sort(key=sort_key)
