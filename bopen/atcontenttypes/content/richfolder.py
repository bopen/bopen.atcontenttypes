"""Definition of the RichFolder content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-
from bopen.atcontenttypes import atcontenttypesMessageFactory as _

from bopen.atcontenttypes.interfaces import IRichFolder
from bopen.atcontenttypes.config import PROJECTNAME

RichFolderSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

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

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

RichFolderSchema['title'].storage = atapi.AnnotationStorage()
RichFolderSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    RichFolderSchema,
    folderish=True,
    moveDiscussion=False
)


class RichFolder(folder.ATFolder):
    """A rich folder"""
    implements(IRichFolder)

    meta_type = "RichFolder"
    schema = RichFolderSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    long_description = atapi.ATFieldProperty('long_description')


atapi.registerType(RichFolder, PROJECTNAME)
