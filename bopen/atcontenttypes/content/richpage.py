"""Definition of the RichPage content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from Products.ATContentTypes.atct import ATDocument, ATDocumentSchema

# -*- Message Factory Imported Here -*-
from bopen.atcontenttypes import atcontenttypesMessageFactory as _

from bopen.atcontenttypes.interfaces import IRichPage
from bopen.atcontenttypes.config import PROJECTNAME

RichPageSchema = ATDocumentSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.ImageField(
        'content_logo',
        storage=atapi.AnnotationStorage(),
        widget=atapi.ImageWidget(
            label=_(u"Content Logo"),
            description=_(u"Field description"),
        ),
        validators=('isNonEmptyFile'),
    ),


    atapi.TextField(
        'long_description',
        storage=atapi.AnnotationStorage(),
        validators = ('isTidyHtmlWithCleanup',),
        default_output_type = 'text/x-html-safe',
        widget=atapi.RichWidget(
            label=_(u"Long Description"),
            description=_(u"Will be shown befor the content body and where long descriptions are needed"),
            rows=10,
        ),
    ),


))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

RichPageSchema['title'].storage = atapi.AnnotationStorage()
RichPageSchema['description'].storage = atapi.AnnotationStorage()

RichPageSchema.moveField('long_description', after='description')

schemata.finalizeATCTSchema(RichPageSchema, moveDiscussion=False)


class RichPage(ATDocument):
    """A rich page"""
    implements(IRichPage)

    meta_type = "RichPage"
    schema = RichPageSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    content_logo = atapi.ATFieldProperty('content_logo')

    long_description = atapi.ATFieldProperty('long_description')


atapi.registerType(RichPage, PROJECTNAME)
