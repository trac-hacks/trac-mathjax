from setuptools import setup

VERSION = '0.1.1'
PACKAGE = 'mathjax'

setup(
    name = 'MathJaxPlugin',
    version = VERSION,
    description = "Renders mathematical equations using MathJax library.",
    author = 'Mitar',
    author_email = 'mitar.trac@tnode.com',
    url = 'http://mitar.tnode.com/',
    keywords = 'trac plugin',
    license = "AGPLv3",
    packages = [PACKAGE],
    include_package_data = True,
    package_data = {
        PACKAGE: ['htdocs/*.js'],
    },
    install_requires = [],
    zip_safe = False,
    entry_points = {
        'trac.plugins': '%s = %s' % (PACKAGE, PACKAGE),
    },
)
