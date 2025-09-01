# -*- coding: utf-8 -*-

from affinitic.smartweb import _
from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from zope import schema
from z3c.relationfield.schema import RelationChoice
from zope.interface import implementer
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives


class ISectionCopyLink(ISection):

    directives.widget(
        "section_link",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "selectableTypes": ["imio.smartweb.SectionText"],
            "favorites": [],
        },
    )
    section_link = RelationChoice(
        title=_("Section to display"),
        vocabulary="plone.app.vocabularies.Catalog",
    )


@implementer(ISectionCopyLink)
class SectionCopyLink(Section):
    pass
