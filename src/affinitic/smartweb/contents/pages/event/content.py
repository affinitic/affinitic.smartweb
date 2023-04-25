# -*- coding: utf-8 -*-

from collective.instancebehavior.interfaces import IInstanceBehaviorAssignableContent
from imio.smartweb.core.contents import IPages
from imio.smartweb.core.contents import Pages
from zope.interface import implementer


class IEvent(IPages):
    """Marker interface and Dexterity Python Schema for Page"""


@implementer(IEvent, IInstanceBehaviorAssignableContent)
class Event(Pages):

    category_name = "event_category"
