import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django_transmission_logging",
    version="0.0.1",
    include_package_data=True,
    author="Coulter Software",
    author_email="info@coultersoftware.ca",
    description="Django Transmission Logging is a simple Django app to standardise the logging of request data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "Django",
        "djangorestframework",
    ],
)