# -*- coding: utf-8 -*-

from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class IImageScales(model.Schema):

    model.fieldset("settings", fields=["image_scale"])
    image_scale = schema.Choice(
        title=_("Image scale for images (only for gallery mode)"),
        default="affiche",
        vocabulary="imio.smartweb.vocabulary.Scales",
        required=True,
    )
