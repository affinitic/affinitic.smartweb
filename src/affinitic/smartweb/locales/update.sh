#!/bin/bash
# i18ndude should be available in current $PATH (eg by running
# ``export PATH=$PATH:$BUILDOUT_DIR/bin`` when i18ndude is located in your buildout's bin directory)
#
# For every language you want to translate into you need a
# locales/[language]/LC_MESSAGES/affinitic.smartweb.po
# (e.g. locales/de/LC_MESSAGES/affinitic.smartweb.po)

domain=affinitic.smartweb
domain_plone=plone

i18ndude rebuild-pot --pot $domain.pot --create $domain ../
i18ndude sync --pot $domain.pot */LC_MESSAGES/$domain.po

i18ndude rebuild-pot --pot $domain_plone.pot --create $domain_plone ../
i18ndude sync --pot $domain_plone.pot */LC_MESSAGES/$domain_plone.po