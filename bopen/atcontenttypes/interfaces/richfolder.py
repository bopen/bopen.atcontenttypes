from zope.interface import Interface
# -*- Additional Imports Here -*-
from zope import schema

from bopen.atcontenttypes import atcontenttypesMessageFactory as _


class IRichFolder(Interface):
    """A rich folder"""

    # -*- schema definition goes here -*-
    long_description = schema.Text(
        title=_(u"Long Description"),
        required=False,
        description=_(u"Will be shown befor the body and where long descriptions are needed"),
    )
#
