# -*- coding: utf-8 -*-
"""Installer for the affinitic.smartweb package."""

from setuptools import find_packages
from setuptools import setup


long_description = "\n\n".join(
    [
        open("README.rst").read(),
        open("CONTRIBUTORS.rst").read(),
        open("CHANGES.rst").read(),
    ]
)


setup(
    name="affinitic.smartweb",
    version="1.0.0a13",
    description="An agnostic version of IMIO Smartweb",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone CMS",
    author="Affinitic",
    author_email="support@affinitic.be",
    url="http://git.affinitic.be/affinitic-addons/affinitic.smartweb",
    project_urls={
        "Source": "http://git.affinitic.be/affinitic-addons/affinitic.smartweb",
        "Tracker": "http://git.affinitic.be/affinitic-addons/affinitic.smartweb/issues",
    },
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["affinitic"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=[
        "setuptools",
        # -*- Extra requirements: -*-
        "plone.api",
        "plone.app.dexterity",
        "plone.restapi",
        "z3c.jbot",
        "imio.smartweb.policy",
        "plone.app.multilingual",
    ],
    extras_require={
        "test": [
            "plone.app.contenttypes",
            "plone.app.iterate",
            "plone.app.robotframework[debug]",
            "plone.app.testing",
            "plone.testing",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = affinitic.smartweb.locales.update:update_locale
    """,
)
