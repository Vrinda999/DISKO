from setuptools import setup, find_packages

setup(
    name="disko",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=open("requirements.txt").read().splitlines(),
    entry_points={
        "console_scripts": [
            "disko = main:main"
        ],
    },
    author="simmithapad",
    description="DISKO: Disk Forensics Tool for Data Categorization & Keyword Filtering",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/simmithapad/DISKO",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.8',
)
