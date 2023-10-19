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


def update_registry(context):
    """
    Update types
    """
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile(
        "profile-affinitic.smartweb:default", "plone.app.registry"
    )


def update_types_event_news(context):
    """
    Update types
    """
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile(
        "profile-affinitic.smartweb:Event and News Types", "typeinfo"
    )
