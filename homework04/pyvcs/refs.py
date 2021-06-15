import pathlib
import typing as tp


def update_ref(gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:
    f = (gitdir / ref).open("w")
    f.write(new_value)
    f.close()


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    f = (gitdir / name).open("w")
    f.write("ref: "+ref+"\n")
    f.close()


def ref_resolve(gitdir: pathlib.Path, refname: str) -> str:
    if refname == "HEAD":
        return resolve_head(gitdir)
    else:
        f = (gitdir / refname)
        if f.exists():
            f = f.open()
            s = f.read()
            f.close()
        else:
            s = None
        return s


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    return ref_resolve(gitdir, get_ref(gitdir))


def is_detached(gitdir: pathlib.Path) -> bool:
    return get_ref(gitdir) is None


def get_ref(gitdir: pathlib.Path) -> str:
    f = (gitdir / "HEAD").open("r")
    s = f.read()
    f.close()
    if s.find("ref: ") == 0:
        s = s[5:-1]
        return s
    else:
        return None
