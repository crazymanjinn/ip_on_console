import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ip_on_console",
    version="0.0.2",
    author="crazymanjinn",
    author_email="crazymanjinn@users.noreply.github.com",
    description="Populates IP address info into /etc/issue.d",
    license="GPLv3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/crazymanjinn/ip_on_console",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        "tabulate",
    ],
    entry_points={
        "console_scripts": [
            "ip_on_console = ip_on_console.main:main",
        ],
    },
    python_requires=">=3, <4",
)
