# from setuptools import setup, find_packages

# setup(
#     name="disko",
#     version="0.1.0",
#     packages=find_packages(),
#     include_package_data=True,
#     install_requires=open("requirements.txt").read().splitlines(),
#     entry_points={
#         "console_scripts": [
#             "disko = main:main"
#         ],
#     },
#     author="simmithapad",
#     description="DISKO: Disk Forensics Tool for Data Categorization & Keyword Filtering",
#     long_description=open("README.md").read(),
#     long_description_content_type="text/markdown",
#     url="https://github.com/simmithapad/DISKO",
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#     ],
#     python_requires='>=3.8',
# )

from setuptools import setup, find_packages

setup(
    name="disko",
    version="1.0.0",
    packages=find_packages(include=["stages", "utils"]),  # include your folders as packages
    py_modules=["main"],  # since main.py is a standalone module
    install_requires=open("requirements.txt").read().splitlines(),
    entry_points={
        "console_scripts": [
            "disko = main:main",  # refers to main() in main.py
        ],
    },
    author="Your Name",
    description="DISKO - Disk Operation Tool for Data Categorization and Keyword Filtering",
    license="MIT",
)
