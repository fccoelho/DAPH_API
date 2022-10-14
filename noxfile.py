from nox_poetry import session
from nox_poetry import Session
from glob import glob
from pathlib import Path


@session(python=["3.10"])
def tests(session):
    session.install("pytest", ".")
    session.install("coverage[toml]", "pytest", "pygments")
    try:
        session.run("coverage", "run", "--parallel", "-m", "pytest", *session.posargs)
    finally:
        if session.interactive:
            session.notify("coverage", posargs=[])

@session
def coverage(session: Session) -> None:
    """Produce the coverage report."""
    args = session.posargs or ["report"]

    session.install("coverage[toml]")

    if not session.posargs and any(Path().glob(".coverage.*")):
        session.run("coverage", "combine")

    session.run("coverage", *args)


@session
def lint(session):
    session.install('autoflake8')
    session.install('black')
    for f in glob('daph_api/*.py', recursive=True):
        session.run('black', f)
        session.run('autoflake8', '--in-place', f)
