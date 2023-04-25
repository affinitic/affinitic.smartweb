# -*- coding: utf-8 -*-

from affinitic.smartweb import _
from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from zope import schema
from zope.interface import implementer


class ISectionEventInfos(ISection):

    display_start = schema.Bool(title=_("Display Start Date"), required=False)

    display_end = schema.Bool(title=_("Display End Date"), required=False)

    display_attendees = schema.Bool(title=_("Display Attendee"), required=False)

    display_contact_email = schema.Bool(title=_("Display Contact Mail"), required=False)

    display_contact_name = schema.Bool(title=_("Display Contact Name"), required=False)

    display_contact_phone = schema.Bool(
        title=_("Display Contact Phone"), required=False
    )

    display_image = schema.Bool(title=_("Display Lead Image"), required=False)

    display_location = schema.Bool(title=_("Display Location"), required=False)

    display_whole_day = schema.Bool(title=_("Display Whole Day"), required=False)

    display_open_end = schema.Bool(title=_("Display Open End"), required=False)

    display_recurrence = schema.Bool(title=_("Display Recurence"), required=False)


@implementer(ISectionEventInfos)
class SectionEventInfos(Section):
    pass
