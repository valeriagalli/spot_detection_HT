"""Installation script for spot-detect."""
from setuptools import setup, find_packages

setup(
    name="spot-detect",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy",
        "scipy",
        "scikit-image",
        "matplotlib",
        "tifffile",
    ],
    python_requires=">=3.10",
)