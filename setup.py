from setuptools import setup
from os import path

this_dir = path.abspath(path.dirname(__file__))

with open(path.join(this_dir, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="alternative_mssql_hook",
    version="0.1",
    packages=["alternative_mssql_hook"],
    author="Arthur Harduim",
    author_email="arthur.harduim@rioenergy.com.br",
    description="Interact with Microsoft SQL Server using sqlalchemy instead of raw pymssql",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={"airflow.plugins": ["mssql_hook = alternative_mssql_hook.mssql_hook:MsSQLHook"]},
    python_requires=">=3.6",
    install_requires=["pymssql", "sqlalchemy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Linux",
    ],
)
