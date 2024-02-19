# -*- coding: utf-8 -*-

from Products.CMFPlone.utils import normalizeString
from datetime import datetime
from dateutil.parser import parse
from imio.smartweb.core.config import EVENTS_URL
from imio.smartweb.core.contents.sections.events.view import EventsView
from imio.smartweb.core.utils import batch_results

import pytz


def naive_to_aware_datetime(date_time):
    utc = pytz.UTC
    return utc.localize(date_time)


class AffiniticEventsView(EventsView):
    """Events Section view"""

    @property
    def items(self):
        today = datetime.today()
        max_items = self.context.nb_results_by_batch * self.context.max_nb_batches
        events = sorted(
            [
                event
                for event in self.context.linking_rest_view.to_object.listFolderContents()
                if event.start > naive_to_aware_datetime(today)
            ],
            key=lambda x: x.start,
        )
        if events is None or len(events) == 0:  # NOQA
            return []
        image_scale = self.image_scale
        items = events[:max_items]
        results = []
        for item in items:
            item_url = item.absolute_url()
            start = item.start
            end = item.end
            date_dict = {"start": start, "end": end}
            image_url = ""
            if item.image:
                image_url = f"{item_url}/@@images/image/{image_scale}"
            results.append(
                {
                    "title": item.title,
                    "description": item.description,
                    "category": item.subject,
                    "event_date": date_dict,
                    "url": item_url,
                    "image": image_url,
                    "has_image": bool(item.image),
                }
            )
        return batch_results(results, self.context.nb_results_by_batch)

    @property
    def see_all_url(self):
        return self.context.linking_rest_view.to_object.absolute_url()

    def is_multi_dates(self, start, end):
        return start and end and start.date() != end.date()
