from setuptools import setup

setup(
    name="package-counter",
    version="1.0",
    description="Check the health of your environments before exporting them",
    python_requires=">=3.7",
    install_requires=["conda"],
    py_modules=["package_counter"],
    entry_points={"conda": ["package-counter = package_counter"]},
)