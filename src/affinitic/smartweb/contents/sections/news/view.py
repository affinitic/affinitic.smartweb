from Products.CMFPlone.utils import normalizeString
from imio.smartweb.core.config import NEWS_URL
from imio.smartweb.core.contents.sections.news.view import NewsView
from imio.smartweb.core.utils import batch_results
from plone import api
from imio.smartweb.core.utils import get_scale_url


class AffiniticNewsView(NewsView):
    """News Section view"""

    def items(self):
        max_items = self.context.nb_results_by_batch * self.context.max_nb_batches
        orientation = self.context.orientation
        news = sorted(
            self.context.linking_rest_view.to_object.listFolderContents(),
            key=lambda x: x.effective_date if x.effective_date else x.creation_date,
        )
        if news is None or len(news) == 0:  # NOQA
            return []
        image_scale = self.image_scale
        results = []
        for item in news[:max_items]:
            url = item.absolute_url()
            scale_url = get_scale_url(
                item, self.request, "image", image_scale, orientation
            )
            dict_item = (
                {
                    "title": item.title,
                    "description": item.description,
                    "category": item.subject,
                    "effective": item.effective_date,
                    "url": url,
                    "has_image": bool(item.image),
                }
            )
            if scale_url == "":
                dict_item["bad_scale"] = image_scale
                scale_url = f"{url}/@@images/image/{image_scale}"
            dict_item["image"] = scale_url
            results.append(dict_item)
        res = batch_results(results, self.context.nb_results_by_batch)
        return res
