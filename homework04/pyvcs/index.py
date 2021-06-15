import binascii
import hashlib
import operator
import os
import pathlib
import struct
import typing as tp

from pyvcs.objects import hash_object


class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        return struct.pack(f">10L20sH{len(self.name.encode())}s3s", self.ctime_s, self.ctime_n, self.mtime_s,
                           self.mtime_n, self.dev, self.ino % 4294967295, self.mode, self.uid, self.gid, self.size, self.sha1,
                           self.flags, self.name.encode(), b"\x00\x00\x00")

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        a = struct.unpack(">10L20sH", data[:62])
        r = GitIndexEntry(
            ctime_s=a[0], ctime_n=a[1], mtime_s=a[2], mtime_n=a[3], dev=a[4], ino=a[5], mode=a[6], uid=a[7],
            gid=a[8], size=a[9], sha1=a[10], flags=a[11], name=data[62:-3].decode()
        )
        return r


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    f = (gitdir / "index")
    if f.exists():
        a = (gitdir / "index").read_bytes()
        length = struct.unpack(">L", a[8:12])[0]
        n = 12
        r = []
        for i in range(0, length):
            p = a.find(b"\x00\x00\x00", n + 62) + 3
            r.append(GitIndexEntry.unpack(a[n:p]))
            n = p
        return r
    else:
        return []


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    a = b"DIRC\x00\x00\x00\x02"
    a += struct.pack(">L", len(entries))
    for i in entries:
        a += i.pack()
    a += hashlib.sha1(a).digest()
    (gitdir / "index").write_bytes(a)


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    for i in read_index(gitdir):
        if details:
            n = 0
            m = i.mode
            for j in range(0, 7):
                n //= 10
                n += m % 8 * 1000000
                m //= 8
            print(f"{n} {i.sha1.hex()} 0\t{i.name}")
        else:
            print(i.name)


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    a = read_index(gitdir)
    dict = {pathlib.Path(i.name): i for i in a}
    names = {pathlib.Path(i.name) for i in a}
    for i in paths:
        if write or i in names:
            st = i.stat()
            sha1 = hash_object(i.read_bytes(), "blob", True, gitdir)
            if i in names:
                a.remove(dict[i])
            a.append(GitIndexEntry(
                ctime_s=st.st_ctime_ns // 1000000000, ctime_n=st.st_ctime_ns % 1000000000,
                mtime_s=st.st_ctime_ns // 1000000000, mtime_n=st.st_mtime_ns % 1000000000, dev=st.st_dev,
                ino=st.st_ino, mode=st.st_mode, uid=st.st_uid, gid=st.st_gid, size=st.st_size, flags=7,
                sha1=binascii.unhexlify(sha1), name=str(i).replace("\\", "/")
            ))
    a.sort(key=lambda x: str(x.name))
    write_index(gitdir, a)
