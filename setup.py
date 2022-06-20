from pathlib import Path
from setuptools import setup, find_packages

APP_ROOT = Path(__file__).parent

INSTALL_REQUIRES = [
    "Flask",
    "Flask-Migrate",
    "Flask-SQLAlchemy",
    "PyJWT",
    "python-dotenv"
]

EXTRAS_REQUIRE = {
    "dev": [
        "flake8",
        "pydocstyle",
        "pytest",
        "pytest-clarity",
        "pytest-dotenv",
        "pytest-flake8",
        "pytest-flask",
        "tox",
    ]
}

setup(
    name='flashcards',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE
)
