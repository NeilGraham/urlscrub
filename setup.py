from setuptools import setup
from os import path, getcwd

setup(
    name="urlscrub",
    version="0.1.0",
    author="Neil Graham",
    author_email="grahamneiln@gmail.com",
    url="https://github.com/NeilGraham/urlscrub",
    license_files="LICENSE.txt",
    description="Tool for parsing URL webpage into JSON + RDF.",
    long_description=open(path.join(getcwd(), "README.md")).read()
    # Replace local links to 'docs/' to Github page 'docs/'.
    .replace(
        "](docs/",
        "](https://github.com/NeilGraham/urlscrub/blob/master/docs/",
    ),
    long_description_content_type="text/markdown",
    packages=["urlscrub"],
    package_dir={"urlscrub": "package"},
    entry_points={"console_scripts": ["urlscrub = urlscrub.__main__:run"]},
    python_requires=">=3.10",
    install_requires=[
        "pytest >= 7.1.2",
        "selenium >= 4.2.0",
        "rdfhash >= 0.3.0",
    ],
)
