# -*- coding: utf-8 -*-

from Acquisition import Implicit
from Acquisition import aq_parent
from affinitic.smartweb import _
from imio.smartweb.core.contents.sections.views import SectionView
from plone import api
from plone.restapi.types.utils import get_info_for_type
from zope.component import getMultiAdapter

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

    # def render_linked(self):
    #     linked = getattr(self.context, 'section_link', None)
    #     if linked and linked.to_object:
            # view = linked.to_object.restrictedTraverse('@@view')

            # return self.context.restrictedTraverse(
            #     f"{linked.to_object.absolute_url_path()}/view/macros/content-core"
            # )

            # view = getMultiAdapter((linked.to_object, self.request), name="view")
            # proxy = ViewProxy(view, can_edit_sections=False)
            # return proxy()
            # view.__dict__['can_edit_sections'] = False
            # setattr(view, "can_edit_sections", False)
            # return view.index()
        # return "<p>No linked section defined.</p>"
    
    # def __call__(self):
    #     linked = getattr(self.context, 'linked_section', None)
    #     if linked and linked.to_object:
    #         view = getMultiAdapter((linked.to_object, self.request), name="view")
    #         return view()
    #     return "No linked section defined."
    