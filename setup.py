import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyMMO",
    version="0.1",
    author="Luis Maior",
    description="PyMMO: A minimalistic library for writing MMO games in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="clone https://github.com/luisoutomaior/PyMMO.git",
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
)