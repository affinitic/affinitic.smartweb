# -*- coding: utf-8 -*-

from Acquisition import aq_parent
from affinitic.smartweb.contents import IEventFolder
from affinitic.smartweb.contents import INewsFolder
from affinitic.smartweb.utils import check_if_folder_exist
from collective.exportimport.import_content import ImportContent
from plone import api
from plone.app.textfield.value import RichTextValue
from plone.i18n.normalizer import idnormalizer
from six.moves.urllib.parse import unquote
from six.moves.urllib.parse import urlparse

import logging
import re
import os

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

    def dict_hook_collage(self, item):
        item["@type"] = "imio.smartweb.Page"
        item["old_type"] = "Collage"
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

    def dict_hook_topic(self, item):
        item["@type"] = "Collection"
        item["layout"] = "view"
        return item

    def _remove_localhost(self, path, plone=True):
        if plone:
            return path.replace("http://localhost:8080/Plone", "")
        return path.replace("http://localhost:8080", "")

    def _path_to_uid(self, path):
        obj = api.content.get(path=self._remove_localhost(path, False))
        if not obj:
            return None, self._remove_localhost(path)
        return obj.UID(), None

    def _handle_link(self, item):
        text = item.get("text", None)
        if not text:
            return item
        data = text.get("data", None)
        if not data:
            return item
        item["text"]["data"] = re.sub(r'(https?:\/\/localhost\:8080\/Plone)', "", data)
        return item

    def dict_hook_publication(self, item):
        ref_ebook = item.get('ref_ebook', None)
        ref_pdf = item.get('ref_pdf', None)
        errors = []
        if ref_ebook:
            item['ref_ebook'], error = self._path_to_uid(ref_ebook)
            if error:
                errors.append(error)
        if ref_pdf:
            item['ref_pdf'], error = self._path_to_uid(ref_pdf)
            if error:
                errors.append(error)

        if len(errors) > 0:
            msg = f"Error : Cannot find {' and '.join(errors)}"

            description = item.get("description", None)
            logger.warning("{} : {}".format(item['@id'], msg))
            if description:
                item['description'] = f"{msg} - {description}"
            else:
                item['description'] = f"{msg}"

        item = self._handle_link(item)

        return item

    def _add_subfolder_in_path(self, path, subfolder, position=-1):
        path_split = path.split("/")
        path_split.insert(position, subfolder)
        return "/".join(path_split)

    def handle_collage_document(self, obj, collage):
        target = collage.get("target", None)
        if target is None:
            return

        if collage["target_type"] == "News Item":
            target = self._add_subfolder_in_path(target, "news")

        # safer path lookup
        site = api.portal.get()
        target_obj = site.unrestrictedTraverse(target.lstrip("/"), None)
        if target_obj is None:
            logger.warning(f"Target not found for collage: {target}")
            return

        sections = target_obj.listFolderContents()
        if not sections:
            logger.info(f"No sections found in target {target}")
            return

        for section in sections:
            # copy via Zope API instead of api.content.copy
            cp = target_obj.manage_copyObjects(ids=[section.getId()])
            result = obj.manage_pasteObjects(cp)

            if result:
                new_id = result[0]['new_id']
                logger.info(
                    "Section %s (%s) copied into %s as %s",
                    section.id,
                    section.portal_type,
                    "/".join(obj.getPhysicalPath()),
                    new_id,
                )
            else:
                logger.warning(
                    "Failed to paste section %s into %s",
                    section.id,
                    "/".join(obj.getPhysicalPath()),
                )

    def handle_collage_image(self, obj, collage):
        target = collage.get("target", None)
        id = collage["id"]
        if target is not None:
            id = target.split("/")[-1]
        api.content.create(
            container=obj,
            type="imio.smartweb.SectionGallery",
            id=id
        )

    def handle_collage_topic(self, obj, collage):
        target = collage.get("target", None)
        if target is None:
            return
        section = api.content.create(
            container=obj,
            type="imio.smartweb.SectionCollection",
            title=collage["title"]
        )
        target_obj = api.content.get(path=target)
        if target_obj and target_obj.portal_type == "Collection":
            section.collection = target_obj

    def handle_collage_news(self, obj, collage):
        target = collage.get("target", None)
        id = collage["id"]
        if target is not None:
            id = target.split("/")[-1]
        section = api.content.create(
            container=obj,
            type="affinitic.smartweb.SectionNews",
            title=collage["title"]
        )
        target_obj = api.content.get(path=target)
        if target_obj and target_obj.portal_type == "Collection":
            section.collection = target_obj

    def handle_collage(self, obj, item):
        collages = item.get("collages", None)
        if collages is None:
            return
        for collage in collages:
            target_type = collage.get("target_type", None)
            if not target_type:
                continue
            adpater = {
                "Document": self.handle_collage_document,
                "Image": self.handle_collage_image,
                "Topic": self.handle_collage_topic,
                "News Item": self.handle_collage_document
            }
            adpater[collage["target_type"]](obj, collage)

    def global_obj_hook(self, obj, item):
        old_type = item.get("old_type", None)
        if old_type and old_type == "Collage":
            self.handle_collage(obj, item)
        return obj

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

    def _create_file_section(self, id, container):
        if id in container:
            return

        section = api.content.create(
            container=container,
            type="imio.smartweb.SectionFiles",
            id=id,
            hide_title=True,
        )
        return section

    def _add_file_to_section(self, section_obj, section_info, context_path):

        file_path = section_info["href"]
        if not file_path.startswith("/Plone/"):
            file_path = os.path.normpath(os.path.join(context_path, file_path))
        file_obj = api.content.get(path=file_path)
        if not file_obj:
            return
        cp = aq_parent(file_obj).manage_copyObjects(ids=[file_obj.getId()])
        result = section_obj.manage_pasteObjects(cp)

        if result:
            new_id = result[0]['new_id']
            logger.info(
                "File %s (%s) copied into %s as %s",
                file_obj.id,
                file_obj.portal_type,
                "/".join(section_obj.getPhysicalPath()),
                new_id,
            )
        else:
            logger.warning(
                "Failed to paste File %s into %s",
                file_obj.id,
                "/".join(section_obj.getPhysicalPath()),
            )

    def _get_gallery_id(self, section):
        if "id" in section:
            return section["id"].replace(".", "-")
        return "_".join(section["merge_data"]).replace(".", "-")

    def global_obj_hook_before_deserializing(self, obj, item):
        """Hook to modify the created obj before deserializing the data."""
        sections_content = item.get("section_content", False)

        if (
            "title" not in item
            or not item["title"]
            or item["title"].replace(" ", "") == ""
        ):
            item["title"] = item["id"]
            logger.warning(
                "{} does not have a title, we take the id ({}) instead".format(
                    item["@id"], item["id"]
                )
            )

        if item["description"] and len(item["description"]) > 700:
            item["description"] = item["description"][:699]
            logger.warning(
                "{} have a descritpion to long, we trim it to 700 characters".format(
                    item["@id"], item["id"]
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
                self._create_gallery_section(
                    id=self._get_gallery_id(section), container=obj
                )

            if section["type"] == "link":
                section_obj = self._create_file_section(
                    id=os.path.basename(section["href"]), container=obj
                )
                self._add_file_to_section(
                    section_obj, section, "/".join(obj.getPhysicalPath())
                )

        return obj, item

    def get_parent_as_container(self, item):
        folder = super(CustomImportDocumentContent, self).get_parent_as_container(item)

        if item["@type"] == "News Item" or item["@type"] == "affinitic.smartweb.News":
            if not check_if_folder_exist(folder, "news", INewsFolder):
                folder = api.content.create(
                    container=folder,
                    type="affinitic.smartweb.NewsFolder",
                    title="News",
                )
            else:
                folder = getattr(folder, "news", False)

        if item["@type"] == "Event" or item["@type"] == "affinitic.smartweb.Event":
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

    def handle_image_container_multi(self, path):
        basename = os.path.basename(path)
        dirname = os.path.dirname(path)
        page = api.content.get(path=dirname)
        if not page:
            return None
        galleries_sections = page.listFolderContents(
            contentFilter={"portal_type": "imio.smartweb.SectionGallery"}
        )
        for section in galleries_sections:
            section_id = section.id
            if basename.replace(".", "-") in section_id:
                return section

    def handle_image_container(self, item):
        section_image = item.get("section_image", None)
        if not section_image:
            return self.get_parent_as_container(item)
        path = section_image.replace("http://localhost:8080", "").replace(".", "-")
        output = api.content.get(path=path)
        if not output:
            output = self.handle_image_container_multi(path)
        return output
