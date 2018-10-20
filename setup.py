import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hourly",
    version="0.0.2",
    author="Asher Pembroke",
    author_email="apembroke@gmail.com",
    description="A simple hour tracker for git",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/asherp/hourly",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)