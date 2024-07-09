# -*- coding: utf-8 -*-

from affinitic.smartweb import _
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import schema
from zope.interface import implementer
from plone.namedfile.field import NamedBlobImage

class IImagePortlet(IPortletDataProvider):
    """A portlet that displays a greeting message."""

    portlet_title = schema.TextLine(
        title = _("Title"),
        required=False
    )

    image = NamedBlobImage(
        title= _("Image")
    )
    
    url = schema.URI(
        title=_('URL'),
        required=False
    )


@implementer(IImagePortlet)
class Assignment(base.Assignment):
    """Portlet assignment."""

    def __init__(self, image=None, portlet_title="", url=None):
        self.image = image
        self.portlet_title = portlet_title
        self.url = url


class Renderer(base.Renderer):
    """Portlet renderer."""

    # Define the page template that will be used to render the portlet
    template = ViewPageTemplateFile("image_portlet.pt")

    def image(self):
        return self.data.image
    
    def portlet_title(self):
        return self.data.portlet_title
    
    def url(self):
        return self.data.url
    
    def portlet_context(self):
        return "/".join(self.data.getPhysicalPath())

    def render(self):
        """This method is called whenever the portlet is rendered."""
        return self.template()


class AddForm(base.AddForm):
    """Portlet add form."""

    schema = IImagePortlet
    label = "Add Greeting Portlet"
    description = "This portlet displays a greeting."

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form."""

    schema = IImagePortlet
    label = "Edit Greeting Portlet"
    description = "This portlet displays a greeting."