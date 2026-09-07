#!/usr/bin/env python3
"""Setup script for 3D Character Agent"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="3d-character-agent",
    version="0.1.0",
    author="Ashish Kumar",
    author_email="ashish.894@yahoo.com",
    description="AI-powered 3D character creation and animation agent for video production",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ashish894-commits/3d-character-agent",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Graphics :: 3D",
        "Topic :: Multimedia :: Video",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "3d-character-agent=src.api.server:main",
        ],
    },
    keywords="3d character animation video blender makehuman ai agent",
    project_urls={
        "Bug Reports": "https://github.com/ashish894-commits/3d-character-agent/issues",
        "Source": "https://github.com/ashish894-commits/3d-character-agent",
        "Documentation": "https://github.com/ashish894-commits/3d-character-agent/tree/main/docs",
    },
)
