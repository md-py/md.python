import pytest

import md.python


class TestReference:
    @pytest.mark.parametrize('definition', ['os.error', 'str'])
    def test_reference_string_definition_returns_it_back(self, definition: str) -> None:  # white/positive
        # act
        reference_ = md.python.reference(definition=definition)

        # assert
        assert reference_ is definition

    def test_reference_builtins_explicit(self) -> None:  # white/positive
        # act
        reference_ = md.python.reference(definition=str)

        # assert
        assert reference_ == 'builtins.str'

    def test_reference_builtins_implicit(self) -> None:  # white/positive
        # act
        reference_ = md.python.reference(definition=str, explicit=False)

        # assert
        assert reference_ == 'str'

    def test_reference_explicit(self) -> None:  # white/positive
        # act
        reference_ = md.python.reference(definition=md.python.reference)

        # assert
        assert reference_ == 'md.python._python.reference'

    def test_reference_implicit_class(self) -> None:  # white/positive
        # act
        reference_ = md.python.reference(definition=TestReference, explicit=False)

        # assert
        assert reference_ == 'python.TestReference'

    def test_reference_implicit(self) -> None:  # white/positive
        # act
        reference_ = md.python.reference(definition=md.python.reference, explicit=False)

        # assert
        assert reference_ == 'md.python.reference'


class TestDereference:
    def test_dereference_explicit(self) -> None:  # white/positive
        # act
        definition = md.python.dereference(reference_='md.python.dereference')

        # assert
        assert definition is md.python.dereference

    def test_dereference_implicit(self) -> None:  # white/positive
        # act
        definition = md.python.dereference(reference_='md.python.dereference')

        # assert
        assert definition is md.python.dereference


class TestVerifyReference:
    @pytest.mark.parametrize('reference_', ['md.python.dereference', 'md.python._python.dereference'])
    def test_verify_reference_explicit(self, reference_: str) -> None:  # white/positive
        # noinspection PyBroadException
        try:
            # act
            md.python.verify_reference(reference_=reference_, source=md.python.dereference)
        except md.python.ReferenceException:
            # assert
            assert False

    @pytest.mark.parametrize('reference_', ['md.python.reference', 'md.python._python.reference'])
    def test_verify_reference_explicit(self, reference_: str) -> None:  # white/negative
        # noinspection PyBroadException
        try:
            # act
            md.python.verify_reference(reference_=reference_, source=md.python.dereference)
        except md.python.ReferenceException as e:
            # assert
            assert e.code == e.DIFFERENT_OBJECT
