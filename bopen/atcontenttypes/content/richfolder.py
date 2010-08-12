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
        searchable=True,
        storage=atapi.AnnotationStorage(),
        validators = ('isTidyHtmlWithCleanup',),
        default_output_type = 'text/x-html-safe',
        widget=atapi.RichWidget(
            label=_(u"Long Description"),
            description=_(u"Will be shown befor the content body and where long descriptions are needed"),
            rows=10,
        ),
    ),


    atapi.ImageField(
        'content_logo',
        original_size=(128, 128),
        sizes={
            'micro': (16, 32),
            'mini': (32, 64),
            'normal': (64, 128),
        },
        storage=atapi.AnnotationStorage(),
        widget=atapi.ImageWidget(
            label=_(u"Content Image"),
            description=_(u"Field description"),
        ),
        validators=('isNonEmptyFile'),
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
    content_logo = atapi.ATFieldProperty('content_logo')

    long_description = atapi.ATFieldProperty('long_description')


atapi.registerType(RichFolder, PROJECTNAME)
