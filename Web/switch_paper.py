import streamlit as st

# import inspect
from importlib import import_module
from typing import Any, Callable, Optional, TypeVar, Union, overload

from streamlit import _gather_metrics

F = TypeVar("F", bound=Callable[..., Any])

# Typing overloads here are actually required so that you can correctly (= with correct typing) use the decorator in different ways:
#   1) as a decorator without parameters @extra
#   2) as a decorator with parameters (@extra(foo="bar") but this also refers to empty parameters @extra()
#   3) as a function: extra(my_function)


@overload
def extra(
    func: F,
) -> F:
    ...


@overload
def extra(
    func: None = None,
) -> Callable[[F], F]:
    ...


def extra(
    func: Optional[F] = None,
) -> Union[Callable[[F], F], F]:

    if func:

        # print(inspect.stack())
        # filename = inspect.stack()[1].filename

        submodule = '__init__' #filename.split("/")[-2]
        extra_name = "streamlit_extras." + submodule
        module = import_module(extra_name)

        if hasattr(module, "__funcs__"):
            module.__funcs__ += [func]  # type: ignore
        else:
            module.__funcs__ = [func]  # type: ignore

        try:
            profiling_name = f"{module}.{func.__name__}"
            return _gather_metrics(name=profiling_name, func=func)
        except ImportError:
            return func

    def wrapper(f: F) -> F:
        return f

    return wrapper



@extra
def switch_page(page_name: str):
    from streamlit.runtime.scriptrunner import RerunData, RerunException
    from streamlit.source_util import get_pages

    def standardize_name(name: str) -> str:
        return name.lower().replace("_", " ")

    page_name = standardize_name(page_name)

    pages = get_pages("UserInfo.py")  # OR whatever your main page is called

    for page_hash, config in pages.items():
        if standardize_name(config["page_name"]) == page_name:
            raise RerunException(
                RerunData(
                    page_script_hash=page_hash,
                    page_name=page_name,
                )
            )

    page_names = [standardize_name(config["page_name"]) for config in pages.values()]

    raise ValueError(f"Could not find page {page_name}. Must be one of {page_names}")


def example():
    want_to_contribute = st.button("I want to contribute!")
    if want_to_contribute:
        switch_page("Contribute")


def test_switch_page():
    import pytest
    from streamlit.runtime.scriptrunner import RerunException

    with pytest.raises(RerunException):
        switch_page("streamlit app")


def test_switch_invalid_page():
    import pytest

    with pytest.raises(ValueError):
        switch_page("non existent page")


__title__ = "Switch page function"
__desc__ = "Function to switch page programmatically in a MPA"
__icon__ = "🖱️"
__examples__ = [example]
__author__ = "Zachary Blackwood"
__tests__ = [test_switch_page, test_switch_invalid_page]
