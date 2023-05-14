from setuptools import setup

setup(
    name="dinos",
    version="0.0.1",
    packages=["dinos"],
    entry_points={"console_scripts" : ["dinos = dinos.__main__:main"]},
    install_requires=["pygame"]
)
