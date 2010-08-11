from zope.interface import Interface
# -*- Additional Imports Here -*-
from zope import schema

from bopen.atcontenttypes import atcontenttypesMessageFactory as _


class IRichPage(Interface):
    """A rich page"""

    # -*- schema definition goes here -*-
    long_description = schema.SourceText(
        title=_(u"Long Description"),
        required=False,
        description=_(u"Field description"),
    )
#
