from typing import List


def remove_duplicates(seq: any) -> List[any]:
    """
    Fast function to remove duplicates while preserving order
    :param seq: iterable to remove duplicates from
    :return: list of the object type from the iterable
    """
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]
