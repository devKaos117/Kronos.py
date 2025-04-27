from setuptools import setup, find_packages

with open("../README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="kronos",
    version="1.0.0",
    author="Gustavo Aragão",
    author_email="gustavo.s.aragao.2003@gmail.com",
    description="A python package to deal with time, analysis and logging",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/devKaos117/Kronos.py",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Logging",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.20.0",
    ]
)