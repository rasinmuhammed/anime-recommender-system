from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="ANIME-RECOMMENDATION-SYSTEM",
    version="0.1",
    author="Muhammed Rasin",
    packages=find_packages(),
    install_requires=requirements,
)