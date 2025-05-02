from setuptools import setup, find_packages

setup(
    name="kronos",
    version="1.0.3",
    author="Gustavo Aragão",
    author_email="gustavo.s.aragao.2003@gmail.com",
    description="A python package to deal with time, analysis and logging",
    long_description="Kronos is a Python utility package for dealing with time, analysis and logging. It was designed to simplify the development of robust, high-performance applications with clean observability and controlled resource usage.",
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
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Logging",
    ],
    python_requires=">=3.8"
)