# md.python

md.python is a component that provides python definition API.

## Architecture overview

![Architecture overview](docs/_static/architecture.class-diagram.png)

## Component overview

```python3
def dereference(reference_: str) -> type: ...
def reference(definition: typing.Union[str, collections.Callable], explicit: bool = True) -> str: ...
def verify_reference(reference_: str, source: object) -> None: ...
```

## Install

```sh
pip install md.python --index-url https://source.md.land/python/
```

## [Documentation](docs/index.md)

Read documentation with examples: https://development.md.land/python/md.python/

# [Changelog](changelog.md)
# [License (MIT)](license.md)
