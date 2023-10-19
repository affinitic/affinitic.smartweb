# -*- coding: utf-8 -*-

from affinitic.smartweb.utils import check_if_folder_exist
from affinitic.smartweb.contents import IEventFolder
from affinitic.smartweb.contents import INewsFolder
from collective.exportimport.import_content import ImportContent
from os.path import join
from plone import api
from plone.app.textfield.value import RichTextValue
from six.moves.urllib.parse import unquote
from six.moves.urllib.parse import urlparse
from plone.i18n.normalizer import idnormalizer

import logging


logger = logging.getLogger(__name__)


class CustomImportDocumentContent(ImportContent):

    PORTAL_TYPE_MAPPING = {
        "Document": "imio.smartweb.Page",
        "Folder": "imio.smartweb.Folder",
    }

    ALLOWED_TYPES = [
        "Collection",
        "Link",
        "imio.smartweb.DirectoryView",
        "imio.smartweb.EventsView",
        "imio.smartweb.Folder",
        "imio.smartweb.NewsView",
        "imio.smartweb.Page",
        "imio.smartweb.PortalPage",
        "imio.smartweb.Procedure",
    ]

    def dict_hook_document(self, item):
        item["@type"] = "imio.smartweb.Page"
        item["layout"] = "full_view"
        return item

    def dict_hook_folder(self, item):
        item["@type"] = "imio.smartweb.Folder"
        item["layout"] = "block_view"
        return item

    def dict_hook_event(self, item):
        item["@type"] = "affinitic.smartweb.Event"
        item["layout"] = "full_view"
        return item

    def dict_hook_newsitem(self, item):
        item["@type"] = "affinitic.smartweb.News"
        item["layout"] = "full_view"
        return item

    def _create_text_section(self, text, title, container):
        if idnormalizer.normalize(title) in container:
            return

        api.content.create(
            container=container,
            type="imio.smartweb.SectionText",
            title=title,
            text=RichTextValue(
                raw=text,
                mimeType="text/html",
                outputMimeType="text/x-html-safe",
            ),
            hide_title=True,
        )

    def _create_gallery_section(self, id, container):
        if id in container:
            return

        api.content.create(
            container=container,
            type="imio.smartweb.SectionGallery",
            id=id,
            hide_title=True,
        )

    def global_obj_hook_before_deserializing(self, obj, item):
        """Hook to modify the created obj before deserializing the data."""
        sections_content = item.get("section_content", False)

        if (
            "title" not in item
            or not item["title"]
            or item["title"].replace(" ", "") == ""
        ):
            item["title"] = item['id']
            logger.warning(
                "{} does not have a title, we take the id ({}) instead".format(
                    item['@id'], item['id']
                )
            )

        if item["description"] and len(item["description"]) > 700:
            item["description"] = item["description"][:699]
            logger.warning(
                "{} have a descritpion to long, we trim it to 700 characters".format(
                    item['@id'], item['id']
                )
            )

        if not sections_content:
            return obj, item

        for count, section in enumerate(sections_content):
            if section["type"] == "text":
                self._create_text_section(
                    text=section["data"],
                    title=f"{item.get('title')} Section Text {count}",
                    container=obj,
                )

            if section["type"] == "image":
                self._create_gallery_section(id=section.get("id"), container=obj)

        return obj, item

    def get_parent_as_container(self, item):
        folder = super(CustomImportDocumentContent, self).get_parent_as_container(item)
        
        if (
            item["@type"] == "News Item"
            or item["@type"] == "affinitic.smartweb.News"
        ):
            if not check_if_folder_exist(folder, "news", INewsFolder):
                folder = api.content.create(
                    container=folder,
                    type="affinitic.smartweb.NewsFolder",
                    title="News",
                )
            else:
                folder = getattr(folder, "news", False)

        if (
            item["@type"] == "Event"
            or item["@type"] == "affinitic.smartweb.Event"
        ):
            if not check_if_folder_exist(folder, "events", IEventFolder):
                folder = api.content.create(
                    container=folder,
                    type="affinitic.smartweb.EventFolder",
                    title="Events",
                )
            else:
                folder = getattr(folder, "events", False)

        return folder

    def create_container(self, item):
        folder = self.context
        parent_url = unquote(item["parent"]["@id"])
        parent_url_parsed = urlparse(parent_url)
        # Get the path part, split it, remove the always empty first element.
        parent_path = parent_url_parsed.path.split("/")[1:]
        if (
            len(parent_url_parsed.netloc.split(":")) > 1
            or parent_url_parsed.netloc == "nohost"
        ):
            # For example localhost:8080, or nohost when running tests.
            # First element will then be a Plone Site id.
            # Get rid of it.
            parent_path = parent_path[1:]

        # create original structure for imported content
        for element in parent_path:
            if element not in folder:
                folder = api.content.create(
                    container=folder,
                    type="imio.smartweb.Folder",
                    id=element,
                    title=element,
                )
                logger.info(
                    "Created container {} to hold {}".format(
                        folder.absolute_url(), item["@id"]
                    )
                )
            else:
                folder = folder[element]

        return folder

    def handle_image_container(self, item):

        path = item["section_image"].replace("http://localhost:8080/Plone", "")
        return api.content.get(path=path)
