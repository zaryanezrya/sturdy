"""
python setup.py test
python3 -m build
twine upload --repository testpypi dist/* # https://upload.pypi.org/legacy/
twine upload --repository pypi dist/* # https://test.pypi.org/legacy/
rm -rf dist sturdy.egg-info
"""

import os
from setuptools import setup, find_packages

import sturdy


here = os.path.dirname(__file__)

with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="sturdy",
    description="Modular app server",
    maintainer="Ivan Sharun",
    maintainer_email="ivan@sha.run",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/omstu-amcs/sturdy",
    license="MIT",
    project_urls={
        "Source": "https://github.com/omstu-amcs/sturdy",
    },
    keywords=["Plugin", "IoC", "Inversion of control", "resolve"],
    version=sturdy.__version__,
    packages=find_packages(),
    test_suite="tests",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)
