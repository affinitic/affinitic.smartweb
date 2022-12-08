FROM docker-prod.affinitic.be/plonetest:6.0

LABEL os="debian" \
    os.version="9" \
    name="affinitic.smartweb" \
    description="affinitic.smartweb test image" \
    maintainer="Affinitic"

USER root

COPY *.rst *.cfg setup.py /plone/
COPY src /plone/src

RUN ls -al /plone

RUN cd /plone \
 && buildout \
 && find /data  -not -user plone -exec chown plone:plone {} \+ \
 && find /plone -not -user plone -exec chown plone:plone {} \+ \
 && find /buildout-cache -not -user plone -exec chown plone:plone {} \+ \
 && rm -rf /Plone*
