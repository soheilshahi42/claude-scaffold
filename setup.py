from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="claude-scaffold",
    version="0.1.0",
    author="Claude Scaffold Team",
    description="Command-line scaffolding tool for self-documenting Claude code projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/claude-scaffold",
    packages=['src'],
    package_dir={'src': 'src'},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "claude-scaffold=src.cli:main",
        ],
    },
    install_requires=[
        "questionary>=2.0.0",
        "colorama>=0.4.6",
        "pyyaml>=6.0",
    ],
    extras_require={
        "dev": ["pytest>=7.0", "black", "flake8", "mypy"],
    },
)