# griptape-labs

[![Tests](https://github.com/griptape-ai/griptape-labs/actions/workflows/tests.yml/badge.svg)](https://github.com/griptape-ai/griptape-labs/actions/workflows/tests.yml)
[![Docs](https://readthedocs.org/projects/griptape/badge/)](https://griptape.readthedocs.io/en/latest/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/gitbucket/gitbucket/blob/master/LICENSE)
[![Griptape Discord](https://dcbadge.vercel.app/api/server/gnWRz88eym?compact=true&style=flat)](https://discord.gg/gnWRz88eym)

Experimental tools and extensions for Griptape.

## Using `griptape-labs`

The Python package in this repo is not on PyPI. We tag the latest stable version with `stable`.

To install it with pip:

```shell
pip install git+https://github.com/griptape-ai/griptape-labs.git@stable
```

Or add it to the `requirements.txt` file:

```
griptape-labs @ git+https://github.com/griptape-ai/griptape-labs.git@stable
```

To install it with Poetry:

```shell
poetry add git+ssh://github.com/griptape-ai/griptape-labs.git#stable
```

Or add it directly to `pyproject.toml`:

```toml
griptape = { git = "https://github.com/griptape-ai/griptape-labs.git", tag = "stable" }
```
