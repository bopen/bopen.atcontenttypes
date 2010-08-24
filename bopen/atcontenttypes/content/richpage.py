"""Definition of the RichPage content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from Products.ATContentTypes.atct import ATDocument, ATDocumentSchema

# -*- Message Factory Imported Here -*-
from bopen.atcontenttypes import atcontenttypesMessageFactory as _

from bopen.atcontenttypes.interfaces import IRichPage, IHaveLongDescription
from bopen.atcontenttypes.interfaces.longdescription import IHaveLongDescription as Z2IHaveLongDescription
from bopen.atcontenttypes.config import PROJECTNAME

RichPageSchema = ATDocumentSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

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
    implements(IRichPage, IHaveLongDescription)
    __implements__ = (getattr(ATDocument,'__implements__',()),) + (Z2IHaveLongDescription,)
    meta_type = "RichPage"
    schema = RichPageSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    content_logo = atapi.ATFieldProperty('content_logo')

    long_description = atapi.ATFieldProperty('long_description')

    # workaround to make resized images:
    # the problem is described on http://plone.293351.n2.nabble.com/ImageField-AttributeStorage-and-Max-Recursion-Depth-Error-td4447134.html
    # so, applied the workaround on http://www.seantis.ch/news/blog/archive/2009/06/22/archetypes-annotationstorage-and-image-scaling
    def __bobo_traverse__(self, REQUEST, name):
        """Transparent access to image scales
        """
        if name.startswith('content_logo'):
            field = self.getField('content_logo')
            image = None
            if name == 'content_logo':
                image = field.getScale(self)
            else:
                scalename = name[len('content_logo_'):]
                if scalename in field.getAvailableSizes(self):
                    image = field.getScale(self, scale=scalename)
            if image is not None and not isinstance(image, basestring):
                # image might be None or '' for empty images
                return image

        return base.ATCTContent.__bobo_traverse__(self, REQUEST, name)

atapi.registerType(RichPage, PROJECTNAME)
