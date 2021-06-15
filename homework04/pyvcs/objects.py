import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False, gitdir: pathlib.Path = None) -> str:
    name = hashlib.sha1(f"{fmt} {len(data)}\0".encode() + data).hexdigest()
    if write:
        if gitdir is None:
            gitdir = repo_find(os.curdir)
        c = gitdir / "objects" / name[0:2]
        if not c.exists():
            c.mkdir()
        c = c / name[2:]
        c.touch()
        c.write_bytes(zlib.compress(f"{fmt} {len(data)}\0".encode() + data))
    return name


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    a = []
    if (len(obj_name) <= 4) | (len(obj_name) >= 40):
        raise Exception(f"Not a valid object name {obj_name}")
    else:
        for i in gitdir.glob("objects/" + obj_name[0:2] + "/" + obj_name[2:] + "*"):
            a.append(str(i.parent.name) + str(i.name))
        if len(a) == 0:
            raise Exception(f"Not a valid object name {obj_name}")
        else:
            return a


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    ...


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    c = gitdir / "objects/" / sha[0:2] / sha[2:]
    b = zlib.decompress(c.read_bytes())
    n = b.find("\0".encode())
    header = b[:n].decode()
    n1 = header.find(" ")
    fmt = header[:n1]
    length = int(header[n1 + 1:])
    content = b[n + 1: n + length + 1]
    return fmt, content


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    a = []
    t = data
    while t.find("\0".encode()) != -1:
        n = t.find(b"\00")
        text = t[:n].decode()
        mode = int(text[:text.find(" ")])
        name = text[text.find(" ") + 1:]
        sha1 = t[n + 1:n + 21].hex()
        a.append((mode, sha1, name))
        t = t[t.find("\0".encode()) + 21:]
    return a


def cat_file(obj_name: str, pretty: bool = True) -> None:
    gitdir = repo_find(os.curdir)
    fmt, content = read_object(obj_name, gitdir)
    if pretty and fmt == "tree":
        a = read_tree(content)
        for i in a:
            mode = i[0]
            name = i[2]
            sha1 = i[1]
            c1 = gitdir / "objects" / sha1[0:2] / sha1[2:]
            b = zlib.decompress(c1.read_bytes())
            header = b[:b.find("\0".encode()) + 1].decode()
            fmt = header[:header.find(" ")]
            if fmt == "tree":
                mode = "040000"
            print(f"{mode} {fmt} {sha1}\t{name}")
    else:
        print(content.decode())


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    # PUT YOUR CODE HERE
    ...


def commit_parse(raw: bytes, start: int = 0, dct=None):
    # PUT YOUR CODE HERE
    ...
