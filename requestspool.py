#!/usr/bin/env python3
"""Multiprocessing pool providing a unique request session per process."""

import itertools
import multiprocessing
import os

import requests

__author__  = "ccc032"
__license__ = "GPLv3"
__version__ = "1.0.0"
__email__   = "ym96@protonmail.ch"


def _split_items(iterable, split_in):
    """Split iterable sequence of items into even subsequences.

    Args:
        iterable:  Iterable sequence of element, like a list or tuple.
        split_in (int): Number of even chunks to split the given sequence in.

    Returns:
        (tuple, list): Defaults to tuple unless `iterable` was a list.
            Tuple/list containing a tuple/list for each subsequence.

    Examples:
    >>> list(_split_items([i for i in range(1, 11)], 3)):
    [[1, 4, 7, 10], [2, 5, 8], [3, 6, 9]]
    """

    if not isinstance(iterable, (list, tuple)):
        iterable = tuple(iterable)

    for i in range(split_in):
        yield iterable[i::split_in]


def _flatten_or_not(flatten, iterable):
    return [i for sub in iterable for i in sub] if flatten else iterable


class RequestsPool(object):
    """Multiprocessing pool providing a unique request session per process.

    Every process started by the `map()` or `starmap()` methods will have a
    unique and constant request session assigned;
    this allows safe requests multiprocessing usage.

    The session will be passed as additional argument to the
    `map()`/`starmap()` target function.

    Attributes:
        processes (int): Number of processes to run in parallel, defaults to
            `os.cpu_count()`.

        special_func (function): Function that will be run to get a specific
            object for each process, defaults to `requests.Session`.

        special_args (tuple): Positional arguments passed to the
            `special_func`, defaults to `()` (no args).

        special_kwargs (dict): Keyword arguments passed to the
            `special_func`, defaults to `{}` (no kwargs).

    Undocumented additional `multiprocessing.Pool` attributes:

        initializer (function): Function ran at the start of a
            `multiprocessing.Pool` worker. Defaults to `None`.

        initargs (tuple): Arguments passed to `initializer`, defaults to `()`.

        maxtasksperchild (int): Maximum number of tasks per process?
            Defaults to `None`.
    """
    def __init__(self, processes=None,
                 special_func=None, special_args=None, special_kwargs=None,
                 initializer=None, initargs=(), maxtasksperchild=None):
        self.processes      = processes      or os.cpu_count()
        self.special_func   = special_func   or requests.Session
        self.special_args   = special_args   or ()
        self.special_kwargs = special_kwargs or {}
        self.pool           = multiprocessing.Pool(processes, initializer,
                                                   initargs, maxtasksperchild)

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        self.pool.close()

    def __getstate__(self):
        """Remove self.pool when pickling to avoid multiprocessing errors."""
        self_dict = self.__dict__.copy()
        del self_dict['pool']
        return self_dict

    def _map_wrap_func(self, func, subsequence):
        special = self.special_func(*self.special_args, **self.special_kwargs)
        return [func(item, special) for item in subsequence]

    def _starmap_wrap_func(self, func, subsequence):
        special = self.special_func(*self.special_args, **self.special_kwargs)
        return [func(*item, special) for item in subsequence]

    def map(self, func, iterable, chunksize=None, flatten=True):
        """Run _map_wrap_func functions, each with split chunks of iterable.

        Example:
            Get multiple pages in parallel, here two at a time:

            >>> URLS = ("https://pypi.org/", "https://git.io",
            ...         "https://gentoo.org")
            >>> def get_url(url, session):
            ...     return session.get(url)
            ...
            >>> with requestspool.RequestsPool(2) as rp:
            ...     print(rp.map(get_url, URLS))
            ...
            [<Response [200]>, <Response [200]>, <Response [200]>]
        """
        return _flatten_or_not(flatten, self.pool.starmap(
            self._map_wrap_func,
            itertools.product((func,), _split_items(iterable, self.processes)),
            chunksize
        ))

    def starmap(self, func, iterable, chunksize=None, flatten=True):
        """Same as map(), but run _map_starmap_func instead.

        Example:
            Get three pages in parallel, pass a same timeout parameter
            to all target function calls, get each processes's results in their
            own sublist:

            >>> from itertools import product

            >>> URLS = ("https://pypi.org/", "https://git.io",
            ...         "https://gentoo.org")

            >>> def get_url_timeout(url, timeout, session):
            ...     return session.get(url, timeout=timeout)
            ...
            >>> with requestspool.RequestsPool(3) as rp:
            ...    print(rp.starmap(get_url_timeout,
            ...                     product(URLS, [6]), flatten=False))
            ...
            [[<Response [200]>], [<Response [200]>], [<Response [200]>]]
        """
        return _flatten_or_not(flatten, self.pool.starmap(
            self._starmap_wrap_func,
            itertools.product((func,), _split_items(iterable, self.processes)),
            chunksize
        ))
