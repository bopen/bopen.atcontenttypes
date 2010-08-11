from zope.interface import Interface
# -*- Additional Imports Here -*-
from zope import schema

from bopen.atcontenttypes import atcontenttypesMessageFactory as _


class IRichFolder(Interface):
    """A rich folder"""

    # -*- schema definition goes here -*-
    content_logo = schema.Bytes(
        title=_(u"Content Image"),
        required=False,
        description=_(u"Field description"),
    )
#
    long_description = schema.Text(
        title=_(u"Long Description"),
        required=False,
        description=_(u"Will be shown befor the body and where long descriptions are needed"),
    )
#
