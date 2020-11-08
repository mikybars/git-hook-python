# Git hooks with Python

This is a demonstration on how to write and set up a simple git hook with Python as scripting language and [Poetry](https://python-poetry.org/docs/basic-usage/) as dependency management tool.

The goal is to have the hook run in an isolated environment (a.k.a. virtualenv) each time, thus not interfering with other libraries or versions already installed on your system.

## Requirements

The only requirement besides a proper installation of Python 3+ is the Poetry tool. In Mac OS X you can install Poetry with Homebrew:

```bash
$ brew install poetry
```

For other systems you may want to check the [documentation](https://python-poetry.org/docs/#installation).

## Install

First grab the tarball with the git hook from the [Releases](https://github.com/mperezi/git-hook-python/releases) section and then issue the following commands:

```bash
$ cd <my-project>/
$ tar xvzf version-enforcer-0.1.0.tgz
x .git/hooks/version-enforcer/
x .git/hooks/version-enforcer/enforce.py
x .git/hooks/version-enforcer/pyproject.toml
x .git/hooks/pre-push
$ (cd .git/hooks/version-enforcer && poetry install)
```

