import os
import pathlib
import typing as tp


def gitname() -> str:
    try:
        git_dir = os.environ["GIT_DIR"]
    except KeyError:
        git_dir = ".git"
    return git_dir


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    git_dir = gitname()
    if workdir is not pathlib.Path:
        workdir = pathlib.Path(workdir)

    found = False
    while not found:
        a = list(workdir.glob(f"*{git_dir}"))
        if a:
            found = True
        else:
            if workdir != workdir.parent:
                workdir = workdir.parent
            else:
                raise Exception("Not a git repository")
    return a[0]


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:

    if workdir is not pathlib.Path:
        workdir = pathlib.Path(workdir)

    git = workdir / gitname()
    if workdir.is_file():
        raise Exception(f"{workdir.name} is not a directory")
    git.mkdir()
    (git / "refs").mkdir()
    (git / "refs/heads").mkdir()
    (git / "refs/tags").mkdir()
    (git / "objects").mkdir()

    f = (git / "HEAD").open("w")
    f.write("ref: refs/heads/master\n")
    f.close()

    f = (git / "config").open("w")
    f.write("[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n")
    f.close()

    f = (git / "description").open("w")
    f.write("Unnamed pyvcs repository.\n")
    f.close()

    return git
