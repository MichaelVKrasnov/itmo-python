import os
import pathlib
import typing as tp

from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, find_object, find_tree_files, read_object, read_tree
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref, ref_resolve
from pyvcs.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    update_index(gitdir, paths)


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    sha = commit_tree(gitdir, write_tree(gitdir, read_index(gitdir)), message, resolve_head(gitdir), author)
    update_ref(gitdir, get_ref(gitdir), sha)
    return sha


def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    a = read_index(gitdir)
    try:
        (gitdir / "index").unlink()
    except FileNotFoundError:
        pass
    for i in a:
        f = pathlib.Path(i.name)
        try:
            f.unlink()
        except FileNotFoundError:
            pass
        while len(os.listdir(f.parent)) == 0:
            f = f.parent
            f.rmdir()
    if (gitdir / "refs/heads" / obj_name).exists():
        c = ref_resolve(gitdir, "refs/heads" + obj_name)
    else:
        c = obj_name

    c = read_object(c, gitdir)[1]
    a = read_tree(read_object(c[5:45].decode(), gitdir)[1])
    paths = []

    while len(a) != 0:
        i = a.pop()
        fmt, data = read_object(i[1], gitdir)
        if fmt == "tree":
            p = pathlib.Path(i[2])
            if not p.exists():
                p.mkdir()
            a.extend([(i1[0], i1[1], str(p / i1[2])) for i1 in read_tree(data)])
        elif fmt == "blob":
            pathlib.Path(i[2]).write_bytes(data)
            paths.append(pathlib.Path(i[2]))

    update_index(gitdir, paths, True)
