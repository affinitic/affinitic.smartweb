# -*- coding: utf-8 -*-

from plone import api
from plone.registry.interfaces import IRegistry
from zope.component import queryUtility
from affinitic.smartweb.utils import uninstall_smartweb_pas_plugins

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


def update_portlet(context):
    """
    Update portlet
    """
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile(
        "profile-affinitic.smartweb:Add Portlet", "portlets"
    )


def uninstall_pas_plugins_kimug(context):
    uninstall_smartweb_pas_plugins(context)