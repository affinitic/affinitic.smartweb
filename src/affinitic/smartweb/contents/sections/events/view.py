# -*- coding: utf-8 -*-

from Products.CMFPlone.utils import normalizeString
from datetime import datetime
from dateutil.parser import parse
from imio.smartweb.core.config import EVENTS_URL
from imio.smartweb.core.contents.sections.events.view import EventsView
from imio.smartweb.core.utils import batch_results
from imio.smartweb.core.utils import get_scale_url

import pytz


def naive_to_aware_datetime(date_time):
    utc = pytz.UTC
    return utc.localize(date_time)


class AffiniticEventsView(EventsView):
    """Events Section view"""

    def items(self):
        today = datetime.today()
        orientation = self.context.orientation
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
            start = item.start
            end = item.end
            date_dict = {"start": start, "end": end}
            url = item.absolute_url()
            scale_url = get_scale_url(
                item, self.request, "image", image_scale, orientation
            )
            dict_item = (
                {
                    "title": item.title,
                    "description": item.description,
                    "category": item.subject,
                    "event_date": date_dict,
                    "url": url,
                    "has_image": bool(item.image),
                }
            )
            if scale_url == "":
                dict_item["bad_scale"] = image_scale
                scale_url = f"{url}/@@images/image/{image_scale}"
            dict_item["image"] = scale_url
            results.append(dict_item)
        return batch_results(results, self.context.nb_results_by_batch)

    @property
    def see_all_url(self):
        return self.context.linking_rest_view.to_object.absolute_url()

    def is_multi_dates(self, start, end):
        return start and end and start.date() != end.date()
