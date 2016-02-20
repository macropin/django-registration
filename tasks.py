from invoke import run
from invoke import task


@task
def clean(docs=False, bytecode=True, extra=''):
    patterns = ['build']
    if docs:
        patterns.append('docs/_build')
    if bytecode:
        patterns.append('**/*.pyc')
    if extra:
        patterns.append(extra)
    for pattern in patterns:
        run("rm -rf %s" % pattern)


@task
def build(docs=False):
    run("python setup.py build")
    if docs:
        run("sphinx-build docs docs/_build")


@task
def test():
    run("python setup.py test")


@task
def lint():
    run("flake8")
