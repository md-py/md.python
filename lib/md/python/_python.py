import builtins
import collections
import importlib
import typing
import types


# Metadata
__author__ = 'https://md.land/md'
__version__ = '1.0.0'
__all__ = (
    # Metadata
    '__author__',
    '__version__',
    # Exception
    'PythonExceptionInterface',
    'ReferenceException',
    'DereferenceException',
    # Public API
    'dereference',
    'reference',
    'verify_reference',
)


# Exception
class PythonExceptionInterface:
    pass


class ReferenceException(PythonExceptionInterface, RuntimeError):
    INVALID_QUALNAME = 1
    IMPORT_ERROR = 2
    DIFFERENT_OBJECT = 3

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.code = 0

    @classmethod
    def as_invalid_qualname(cls) -> 'ReferenceException':
        exception = cls()  # Unable to resolve `{class_qualname}`, absolute path is required
        exception.code = cls.INVALID_QUALNAME
        return exception

    @classmethod
    def as_import_error(cls) -> 'ReferenceException':
        exception = cls()
        exception.code = cls.IMPORT_ERROR
        return exception

    @classmethod
    def as_different_object(cls) -> 'ReferenceException':
        exception = cls()
        exception.code = cls.DIFFERENT_OBJECT
        return exception


class DereferenceException(PythonExceptionInterface, RuntimeError):
    INVALID_QUALNAME = 1
    IMPORT_ERROR = 2

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.code = 0

    @classmethod
    def as_invalid_qualname(cls) -> 'DereferenceException':
        exception = cls()  # Unable to resolve `{class_qualname}`, absolute path is required
        exception.code = cls.INVALID_QUALNAME
        return exception

    @classmethod
    def as_import_error(cls) -> 'DereferenceException':
        exception = cls()
        exception.code = cls.IMPORT_ERROR
        return exception


# Public API
def dereference(reference_: str) -> object:
    """ Dereferences string class pointer to a code entity object """
    assert all([part.isidentifier() for part in reference_.split('.')])

    try:
        module_name, definition_name = reference_.rsplit('.', 1)
    except ValueError as e:
        try:  # for optimization purposes only
            return getattr(builtins, reference_)
        except AttributeError:
            raise DereferenceException.as_import_error() from e

    try:
        module: types.ModuleType = importlib.import_module(name=module_name)
    except (ModuleNotFoundError, AttributeError) as e:
        raise DereferenceException.as_import_error() from e

    try:
        return getattr(module, definition_name)
    except AttributeError as e:
        raise DereferenceException.as_invalid_qualname() from e


# noinspection PyUnresolvedReferences
def reference(definition: typing.Union[str, collections.Callable], explicit: bool = True) -> str:
    """ References class object to a string pointer """
    if isinstance(definition, str):
        assert all([part.isidentifier() for part in definition.split('.')])
        return definition  # as is

    if not getattr(definition, '__module__', None):
        raise NotImplementedError(f'Type `{type(definition)}` not supported yet')

    assert all([part.isidentifier() for part in definition.__module__.split('.')])
    module_reference: str = definition.__module__  # md.python._python

    if explicit:
        # e.g. reference(os.error) -> 'os.error',
        # e.g. reference(str) -> 'builtins.str'
        # e.g. reference(md.python.reference) -> 'md.python._python.reference'
        return f'{module_reference}.{definition.__name__}'

    if '._' in module_reference:
        # if reference is explicit, resolve implicit version of it
        # e.g. `md.python._python.reference` -> `md.python.reference`
        if module_reference.count('._') != 1:
            raise NotImplementedError

        path = module_reference.split('.')  # e.g. `['md', 'python', '_python']`
        if f'_{path[-2]}' == path[-1]:  # this check can be omitted, when verification enabled
            module_reference = '.'.join(path[:-1])  # e.g. `md.python`
        return f'{module_reference}.{definition.__name__}'  # e.g. `md.python.reference`

    if module_reference == 'builtins':
        return definition.__name__  # e.g. reference(str) -> 'str'

    if isinstance(definition, type):
        return f'{module_reference}.{definition.__name__}'

    return definition.__class__.__name__  # as is


def verify_reference(reference_: str, source: object) -> None:
    try:
        module_reference, definition = reference_.rsplit('.', 1)
    except ValueError as exception:
        raise ReferenceException.as_invalid_qualname() from exception

    try:
        module = importlib.import_module(name=module_reference)
    except (ModuleNotFoundError, TypeError) as exception:
        raise ReferenceException.as_import_error() from exception

    try:
        destination = getattr(module, definition)
    except AttributeError as exception:  # yes, not `hasattr` check for exception chaining
        raise ReferenceException.as_import_error() from exception

    if destination is not source:
        raise ReferenceException.as_different_object()
