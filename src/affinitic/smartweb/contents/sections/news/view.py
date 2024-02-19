from Products.CMFPlone.utils import normalizeString
from imio.smartweb.core.config import NEWS_URL
from imio.smartweb.core.contents.sections.news.view import NewsView
from imio.smartweb.core.utils import batch_results
from plone import api


class AffiniticNewsView(NewsView):
    """News Section view"""

    @property
    def items(self):
        max_items = self.context.nb_results_by_batch * self.context.max_nb_batches
        news = sorted(
            self.context.linking_rest_view.to_object.listFolderContents(),
            key=lambda x: x.effective_date if x.effective_date else x.creation_date,
        )
        if news is None or len(news) == 0:  # NOQA
            return []
        image_scale = self.image_scale
        results = []
        for item in news[:max_items]:
            item_url = item.absolute_url()
            image_url = ""
            if item.image:
                image_url = f"{item_url}/@@images/image/{image_scale}"
            results.append(
                {
                    "title": item.title,
                    "description": item.description,
                    "category": item.subject,
                    "effective": item.effective_date,
                    "url": item_url,
                    "image": image_url,
                    "has_image": bool(item.image),
                }
            )
        res = batch_results(results, self.context.nb_results_by_batch)
        return res
