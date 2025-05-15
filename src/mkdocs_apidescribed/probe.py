"""This is a module description.

This takes several lines and contains formatted text.

https://github.com/idlesign/mkdocs-apidescribed-plugin

!!! note
    This text is an admonition.

.. warning:: This is a reStructuredText mixed warning.
"""
from os import environ

from markdown.util import deprecated

CONSTANT: int = 1
"""Constant description."""

ENVIRON = environ
"""Alias description."""


def undocumented():  # pragma: nocover
    pass


def _hidden():
    """Hide it."""


def just_ignore_that():
    """Ignore it."""


def myfunc_rst(
    a: list[str],
    b: int = 0,
    *args,
    another: str,
    **kwargs
) -> bool:
    """Function description.
    This one is split into several lines
    yet supposes a single sentence.

    Uses reStructuredText markup for signature description.

    See: https://github.com/idlesign/mkdocs-apidescribed-plugin

    .. note::
        Some note here.

    .. code-block:: bash
        cd ~
        touch this/

    :param a: comment for a
        .. versionadded:: 2.5
            Add this.

        .. versionchanged:: 2.5
            Something has changed.

    :type a: List[str], optional
    :param b: hint for b
        Several lines.

        .. warning::
            Some warning

        Another line.
        https://github.com/idlesign/mkdocs-apidescribed-plugin
    :param args: info for args
    :param another: text for another
        .. deprecated:: 3.1
            Use something instead.

    :param kwargs: description for kwargs

    :raises ValueError: If something happens
    :raises KeyError: If something other happens

    :return: This is returned
    :return: This is also returned
    :rtype: bool

    """


def myfunc_google(q: str, w: int, e: list, **kwargs) -> bool:
    """Function description.

    Uses Google markup for signature description.

    Note:
        Some note for you.

    Args:
        q (str): Param q
        w: Param w
        e: Param e
        **kwargs: Keyword parameters

    Yields:
        int: This one

    Returns:
        bool: True if successful, False otherwise.

        Even more text for return description.

    Raises:
        AttributeError: Can raise
            this in some cases.
        ValueError: If something.

    Examples:
        This is an example.
        Multiple Lines.

    """


class MyBaseClass:
    """Base class description."""

    base_attr: str = "base_attr value"
    """Base attr description."""

    @classmethod
    def method_cl(cls, arg1: str):
        """Class method."""

    @staticmethod
    def method_st(cls, val):
        """Static method."""

    def __init__(self, in_a: int):
        """Base __init__ description."""

    def __call__(self, in_b: int):
        """Base __call__ description."""

    @property
    def prop_a(self) -> str:
        """Property A."""

    @prop_a.setter
    def _prop_a_set(self, val: int) -> str:
        """Property A setter."""

    def __str__(self):
        """Specialized. To string."""

    def method_a(self, a=1):  # pragma: nocover
        """Base method_a description."""
        return True


class MySubClass(MyBaseClass, list):
    """Sub class description."""

    sub_attr = "sub_attr value"
    """Sub attr description."""

    @deprecated('This one is deprecated.')
    def method_sub_b(
        self,
        a: str,
        b: int,
        d: float,
    ) -> str:  # pragma: nocover
        """Sub method_sub_b description."""
        return ''
