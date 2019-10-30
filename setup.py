import os.path
import re

import setuptools


def read(*parts):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, *parts)) as f:
        return f.read()


def find_version(*file_parts):
    version_file = read(*file_parts)
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]$", version_file, re.M
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setuptools.setup(
    name="txt2tags",
    version=find_version("txt2tags.py"),
    description="Convert between markup languages",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords="markup",
    url="https://txt2tags.org",
    author="Aurelio Jargas",
    author_email="aurelio@aurelio.net",
    maintainer="Jendrik Seipp",
    maintainer_email="jendrikseipp@gmail.com",
    license="GPL2+",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: X11 Applications",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Text Processing :: Markup",
    ],
    py_modules=["txt2tags"],
    entry_points={"console_scripts": ["txt2tags=txt2tags:exec_command_line"]},
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    tests_require=["tox"],
)
