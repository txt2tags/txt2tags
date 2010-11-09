from setuptools import setup

setup(
    name = "txt2tags",
    version = '2.6',
    url = 'http://txt2tags.org',
    author = 'Aurelio Jargas',
    author_email = 'verde@aurelio.net',
    description = "Document generator. Reads a text file with minimal markup as **bold** and //italic// and converts it to various formats",
    long_description=open('README').read(),
    include_package_data = True,
    scripts = ['txt2tags',],
)
