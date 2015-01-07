from setuptools import setup

setup(
    name='xo_server',
    version='1.0',
    author='Alexei Romanov',
    author_email='drednout.by@gmail.com',
    description = ("Simple game server for XO game"),
    license="GPLv2",
    keywords="game server xo",
    url="https://github.com/drednout/xo_server",
    packages=['xo_server'],
    long_description=open('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Games/Entertainment :: Board Games",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
)
