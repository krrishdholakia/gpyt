import secrets
import string
import os
from pathlib import Path


_ALPHABET = string.hexdigits


def get_id(length=16) -> str:
    _id = "".join([secrets.choice(_ALPHABET) for _ in range(length)])
    if _id in get_id.seen:
        return get_id(length)
    return _id


# TODO: load previous convo and message ids to ensure no overlap (pretty unlikely though lol)
get_id.seen = set()

if __name__ == "__main__":
    HOME_DIR = os.getenv("HOME")
    assert HOME_DIR, "Missing $HOME env var"
    os.makedirs(Path(HOME_DIR, ".cache", "gpyt", "conversations"))
