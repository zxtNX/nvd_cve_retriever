from setuptools import setup, find_packages

setup(
    name="nvd_cve_retriever",
    version="0.1.0",
    description="Ce programme permet de récupérer les CVEs via l'API de NVD",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="zxtNX",
    platforms=["Any"],
    packages=find_packages(),
    install_requires=[
        "requests",
        "colorama",
        "python-dotenv",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "nvd_cve_retriever=nvd_cve_retriever.__main__:main",
        ],
    },
)
