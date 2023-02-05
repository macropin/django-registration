from invoke import run
from invoke import task


@task
def clean(ctx, all=False):
    if all:
        flag = "--all"
    else:
        flag = ""
    run("python setup.py clean {}".format(flag))


@task
def build(ctx, docs=False):
    run("python setup.py build")
    if docs:
        run("sphinx-build docs docs/_build")


@task
def test(ctx):
    run("python setup.py test")


@task
def lint(ctx):
    run("rst2html.py README.rst > /dev/null")
    run("flake8 registration")
    run("isort --recursive --check-only registration")
