import pytest

from envawareconfig.expand_variables import expand_variables
from envawareconfig import MissingEnvVarError


def test_text_is_returned_untouched_if_it_has_nothing_to_expand():
    text = "This has nothing to expand."
    expected = text
    actual = expand_variables(text=text, context={"key": "value"})
    assert actual == expected


def test_variable_is_expanded_successfully_with_value_in_context():
    text = "This is a ${ADJECTIVE} expansion."
    expected = "This is a wonderful expansion."
    actual = expand_variables(text=text, context={"ADJECTIVE": "wonderful"})
    assert actual == expected


def test_variable_is_expanded_successfully_with_default_value():
    text = "This is a ${ADJECTIVE:marvelous} expansion."
    expected = "This is a marvelous expansion."
    actual = expand_variables(text=text, context={})
    assert actual == expected


def test_error_is_raised_if_no_replacement_nor_default_is_found():
    text = "This ${NONEXISTENT} will cause an error."
    with pytest.raises(MissingEnvVarError):
        expand_variables(text=text, context={})
