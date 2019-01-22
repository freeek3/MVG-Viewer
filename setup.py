import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="WorkAutomation",
    version="1.0",
    author="Lars Müller",
    author_email="lars.mueller@lehn-partner.com",
    description="A small Package which i use at Work",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/freeek3/WorkAutomation",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'mvgviewer = mvg:main',
            'timetracker = timetracker:main'
        ],
    },
    package_data={'': ['mvg\\icon.ico']},
    include_package_data=True,
)
