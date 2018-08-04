#!/usr/bin/env python3
"""requestspool setuptools file"""

from setuptools import setup
import requestspool

setup(
    name       = requestspool.__name__,
    version    = requestspool.__version__,
    py_modules = ["requestspool"],

    author       = requestspool.__author__,
    author_email = requestspool.__email__,
    description  = requestspool.__doc__,
    license      = requestspool.__license__,
    keywords     = "multiprocessing pool parallel requests session",
    url          = "https://github.com/ccc032/requestspool",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "Topic :: Internet :: WWW/HTTP :: Session",

        "License :: OSI Approved :: GNU Lesser General Public License v3 "
        "or later (LGPLv3+)",

        "Programming Language :: Python :: 3.6",

        "Natural Language :: English",

        "Operating System :: POSIX :: Linux",
    ]
)
