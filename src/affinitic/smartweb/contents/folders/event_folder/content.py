# -*- coding: utf-8 -*-

from collective.instancebehavior.interfaces import IInstanceBehaviorAssignableContent
from imio.smartweb.core.contents import IFolder
from imio.smartweb.core.contents import Folder
from zope.interface import implementer


class IEventFolder(IFolder):
    pass


@implementer(IEventFolder, IInstanceBehaviorAssignableContent)
class EventFolder(Folder):
    pass
