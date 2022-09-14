from nox_poetry import session
from glob import glob

@session(python=["3.10"])
def tests(session):
    session.install("pytest", ".")
    session.run("pytest")

@session
def lint(session):
    session.install('autoflake8')
    session.install('black')
    for f in glob('daph_api/*.py', recursive=True):
        session.run('black', f)
        session.run('autoflake8', '--in-place', f)