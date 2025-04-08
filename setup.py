from setuptools import setup, find_packages

setup(
    name="unitflex",
    version="0.8.0",  
    author="zranndts",
    author_email="vleaxorzz@gmail.com",
    description="Unit Converter Library",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/zranndts/unitflex",
    packages=find_packages(),  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6", 
    install_requires=[], 
)
