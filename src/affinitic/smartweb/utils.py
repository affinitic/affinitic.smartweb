from imio.smartweb.locales import SmartwebMessageFactory as _isw
from plone.i18n.normalizer import IIDNormalizer
from plone import api
from zope.component import getUtility
from zope.i18n import translate
from Products.CMFCore.interfaces import IFolderish

def delete_i_am_i_find_folders(context):
    # TODO: context could be the Plone Site OR a Language Root Folder; handle both cases

    normalizer = getUtility(IIDNormalizer)
    lang = api.portal.get_current_language()[:2]

    for title in ("I am", "I find"):
        translated_title = translate(_isw(title), target_language=lang)
        translated_id = normalizer.normalize(translated_title)
        if translated_id in context:
            api.content.remove(id=translated_id)

def check_if_folder_exist(context, folder_id):
    if getattr(context, folder_id, False):
        if IFolderish.providedBy(context[folder_id]):
            return True
        else:
            raise TypeError(f"Item {folder_id} exist but not a folder")
    else:
        return False