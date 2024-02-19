# -*- coding: utf-8 -*-

from Acquisition import aq_parent
from affinitic.smartweb import _
from imio.smartweb.core.contents.sections.views import SectionView
from plone import api
from plone.restapi.types.utils import get_info_for_type

import locale


def adapter_default(data):
    return data


def adapter_date(data):
    locale.setlocale(locale.LC_TIME, f"{api.portal.get_current_language()}_BE")
    return data.strftime("%d %B %Y %H:%M")


def adapter_bool(data):
    if data:
        return _("Yes")
    return _("No")


DISPLAY_FIELD = {
    "start": adapter_date,
    "end": adapter_date,
    "attendees": adapter_default,
    "contact_email": adapter_default,
    "contact_name": adapter_default,
    "contact_phone": adapter_default,
    "image": adapter_default,
    "location": adapter_default,
    "whole_day": adapter_bool,
    "open_end": adapter_bool,
    "recurrence": adapter_default,
}


class EventInfosView(SectionView):
    def __init__(self, context, request):
        super(EventInfosView, self).__init__(context, request)
        self.section_settings = context
        self.event_context = aq_parent(context)
        self.event_schema = get_info_for_type(
            self.event_context, self.request, "affinitic.smartweb.Event"
        )

    def get_values(self):
        response = []
        for field in DISPLAY_FIELD:
            if getattr(self.section_settings, f"display_{field}", None) and getattr(
                self.event_context, field, None
            ):
                response.append(
                    {
                        "field": {
                            "id": field,
                            "title": self.event_schema["properties"][field]["title"],
                        },
                        "value": DISPLAY_FIELD[field](
                            getattr(self.event_context, field, "")
                        ),
                    }
                )

        return response
