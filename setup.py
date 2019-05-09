from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    """
    Run tests with "python setup.py test".
    """
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import subprocess
        import sys
        errno = subprocess.call([sys.executable, 'run.py'], cwd='test')
        sys.exit(errno)

setup(
    name = "txt2tags",
    version = '3.0',
    url = 'http://txt2tags.org',
    author = 'Aurelio Jargas',
    author_email = 'verde@aurelio.net',
    description = "Document generator. Reads a text file with minimal markup as **bold** and //italic// and converts it to various formats",
    long_description=open('README').read(),
    include_package_data = True,
    scripts = ['txt2tags',],
    cmdclass = {'test': PyTest},
)
