# -*- coding: utf-8 -*-

from plone import api


def update_types(context):
    """
    Update types
    """
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile(
        "profile-affinitic.smartweb:default", "typeinfo"
    )
