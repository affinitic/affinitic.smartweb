# -*- coding: utf-8 -*-

from collective.instancebehavior.interfaces import IInstanceBehaviorAssignableContent
from imio.smartweb.core.contents import Folder
from imio.smartweb.core.contents import IFolder
from zope.interface import implementer


class INewsFolder(IFolder):
    pass


@implementer(INewsFolder, IInstanceBehaviorAssignableContent)
class NewsFolder(Folder):
    pass
