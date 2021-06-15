import os
import pathlib
import stat
import time
import typing as tp
from binascii import unhexlify

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    a = b""
    for i in index:
        if pathlib.Path(i.name).parent == gitdir.parent / dirname:
            n = 0
            m = i.mode
            for j in range(0, 7):
                n //= 10
                n += m % 8 * 1000000
                m //= 8
            a += f"{n} {pathlib.Path(i.name).name}\0".encode() + i.sha1
        else:
            try:
                folder = pathlib.Path(i.name).relative_to(gitdir.parent / dirname).parents[0]
            except ValueError:
                continue
            else:
                n = 0
                m = folder.stat().st_mode
                for j in range(0, 7):
                    n //= 10
                    n += m % 8 * 1000000
                    m //= 8
                a += f"{40000} {folder}\0".encode() + unhexlify(write_tree(gitdir, index, str(folder)))
    return hash_object(a, "tree", True)


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    a = f"tree {tree}\n".encode()
    t = str(int(time.mktime(time.localtime()))) + " " + str(time.strftime("%z", time.localtime()))
    if parent is not None:
        a += f"parent {parent}\n".encode()
    if author is None:
        author = os.getenv("GIT_AUTHOR_NAME", None) + " " + f'<{os.getenv("GIT_AUTHOR_EMAIL", None)}>'
    a += f"author {author} {t}\n".encode()
    a += f"committer {author} {t}\n".encode()
    a += f"\n{message}\n".encode()
    return hash_object(a, "commit", True)
