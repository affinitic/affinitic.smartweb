# -*- coding: utf-8 -*-

from Acquisition import Implicit
from Acquisition import aq_parent
from affinitic.smartweb import _
from imio.smartweb.core.contents.sections.views import SectionView
from plone import api
from plone.restapi.types.utils import get_info_for_type
from zope.component import getMultiAdapter
from imio.smartweb.core.utils import get_scale_url

import locale


class ViewProxy(Implicit):
    def __init__(self, view, **kwargs):
        self._view = view
        self.__dict__.update(kwargs)

    def __getattr__(self, name):
        return getattr(self._view, name)

    def __call__(self, *args, **kwargs):
        # temporarily disable redirect
        response = self._view.request.response
        redirect = getattr(response, 'redirect', None)
        if redirect:
            response.redirect = lambda url, *a, **kw: None
        result = self._view(*args, **kwargs)
        if redirect:
            response.redirect = redirect
        return result


class SectionCopyLinkView(SectionView):
    def get_context(self):
        linked = getattr(self.context, 'section_link', None)
        if not (linked and linked.to_object):
            return None
        return self.context.section_link.to_object

    def get_scale_url(self, item, scale="vignette"):
        orientation = self.context.orientation
        if item.portal_type == "imio.smartweb.SectionGallery":
            images = item.getObject().listFolderContents()
            if not images:
                return ""
            scale_url = get_scale_url(
                images[0], self.request, "image", scale, orientation
            )
            return scale_url
        return get_scale_url(item, self.request, "image", scale, orientation)