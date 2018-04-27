#!/bin/python3
"""requestspool simple tests"""

from itertools import product

from requestspool import RequestsPool

URLS = ("https://pypi.org/", "https://git.io", "https://gentoo.org")


print("map() Test:")

def get_url(url, session):
    return session.get(url)

with RequestsPool(2) as rp:
    print(rp.map(get_url, URLS))


print("\nstarmap() Test:")

def get_url_timeout(url, timeout, session):
    return session.get(url, timeout=timeout)

with RequestsPool(3) as rp:
    print(rp.starmap(get_url_timeout, product(URLS, (6,))))
