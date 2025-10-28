from Products.CMFCore.interfaces import IFolderish
from imio.smartweb.locales import SmartwebMessageFactory as _isw
from plone import api
from plone.i18n.normalizer import IIDNormalizer
from zope.component import getUtility
from zope.i18n import translate
from plone.registry.interfaces import IRegistry
from zope.component import queryUtility

def delete_i_am_i_find_folders(context):
    # TODO: context could be the Plone Site OR a Language Root Folder; handle both cases
    portal = api.portal.get()
    normalizer = getUtility(IIDNormalizer)
    lang = api.portal.get_current_language()[:2]
    for title in ("I am", "I find"):
        translated_title = translate(_isw(title), target_language=lang)
        translated_id = normalizer.normalize(translated_title)
        if translated_id in portal:
            api.content.delete(obj=portal[translated_id])


def uninstall_smartweb_pas_plugins(context):
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runAllImportStepsFromProfile(
        "profile-pas.plugins.kimug:uninstall"
    )
    portal_setup.runAllImportStepsFromProfile(
        "profile-pas.plugins.oidc:uninstall"
    )
    registry = queryUtility(IRegistry)
    if "plone.external_login_url" in registry:
        registry["plone.external_login_url"] = ""
    if "plone.external_logout_url" in registry:
        registry["plone.external_logout_url"] = ""


def check_if_folder_exist(context, folder_id, interface=IFolderish):
    folder = getattr(context, folder_id, None)
    if folder:
        if interface.providedBy(folder):
            return True
        else:
            return False
    else:
        return False
