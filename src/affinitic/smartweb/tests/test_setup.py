# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from Products.CMFPlone.utils import get_installer
from affinitic.smartweb import testing  # noqa: E501
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class TestSetup(unittest.TestCase):
    """Test that affinitic.smartweb is properly installed."""

    layer = testing.AFFINITIC_SMARTWEB_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if affinitic.smartweb is installed."""
        self.assertTrue(self.installer.is_product_installed("affinitic.smartweb"))

    def test_browserlayer(self):
        """Test that IAffiniticSmartwebLayer is registered."""
        from affinitic.smartweb.interfaces import IAffiniticSmartwebLayer
        from plone.browserlayer import utils

        self.assertIn(IAffiniticSmartwebLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = testing.AFFINITIC_SMARTWEB_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("affinitic.smartweb")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if affinitic.smartweb is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("affinitic.smartweb"))

    def test_browserlayer_removed(self):
        """Test that IAffiniticSmartwebLayer is removed."""
        from affinitic.smartweb.interfaces import IAffiniticSmartwebLayer
        from plone.browserlayer import utils

        self.assertNotIn(IAffiniticSmartwebLayer, utils.registered_layers())
