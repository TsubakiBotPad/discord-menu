import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="discord-menu",
    version="0.7.0",
    author="The Tsubotki Team",
    author_email="69992611+TsubakiBotPad@users.noreply.github.com",
    license="Apache-2.0 License",
    description="A library to create tabbed menus in Discord messages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TsubakiBotPad/discord-menu",
    packages=setuptools.find_packages(),
    install_requires=[""],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
