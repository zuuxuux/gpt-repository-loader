from setuptools import setup, find_packages

setup(
    name="gpt-repository-loader",
    version="0.1.0",
    author="mpoon",
    description="A tool that converts the contents of a Git repository into a text format.",
    url="https://github.com/mpoon/gpt-repository-loader",
    packages=find_packages(),
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'gpt-repository-loader=gpt_repository_loader.gpt_repository_loader:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    },
)
