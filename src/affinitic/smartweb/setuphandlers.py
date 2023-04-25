# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from affinitic.smartweb.utils import delete_i_am_i_find_folders
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "affinitic.smartweb:uninstall",
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.

    delete_i_am_i_find_folders(context)


def post_install_types(context):
    """Post install script"""
    # Do something at the end of the installation of this package.


def post_install_portlets(context):
    """Post install script"""
    # Do something at the end of the installation of this package.


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
