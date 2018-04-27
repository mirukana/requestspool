# requestspool

Multiprocessing pool providing an unique request session per process,
thus avoiding the common problems like SSL errors when trying to use a
global session for multiple processes.

Every process started by the `map()` or `starmap()` methods will have a
session assigned.

The session will be passed as additional argument to the
`map()`/`starmap()` target function.

## Examples

Get multiple pages in parallel, here two at a time:

    >>> URLS = ("https://pypi.org/", "https://git.io",
    ...         "https://gentoo.org")
    >>> def get_url(url, session):
    ...     return session.get(url)
    ...
    >>> with requestspool.RequestsPool(2) as rp:
    ...     print(rp.map(get_url, URLS))
    ...
    [[<Response [200]>, <Response [200]>], [<Response [200]>]]

Get three pages in parallel and pass a same timeout parameter
to all target function calls:

    >>> from itertools import product
    >>> URLS = ("https://pypi.org/", "https://git.io",
    ...         "https://gentoo.org")
    >>> def get_url_timeout(url, timeout, session):
    ...     return session.get(url, timeout=timeout)
    ...
    >>> with requestspool.RequestsPool(3) as rp:
    ...    print(rp.starmap(get_url_timeout, product(URLS, (6,))))
    ...
    [[<Response [200]>], [<Response [200]>], [<Response [200]>]]

## Installation

Requires Python 3 (currently only tested on **3.6.5** with GNU/Linux).

From **pip**:

    sudo pip3 install requestspool

Manually:

      git clone https://github.com/ccc032/requestspool
      cd requestspool
      sudo python3 setup.py install 
