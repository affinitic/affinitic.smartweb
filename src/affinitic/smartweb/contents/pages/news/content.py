# -*- coding: utf-8 -*-

from collective.instancebehavior.interfaces import IInstanceBehaviorAssignableContent
from imio.smartweb.core.contents import IPages
from imio.smartweb.core.contents import Pages
from zope.interface import implementer


class INews(IPages):
    """Marker interface and Dexterity Python Schema for News Item"""


@implementer(INews, IInstanceBehaviorAssignableContent)
class News(Pages):

    category_name = "news_category"
