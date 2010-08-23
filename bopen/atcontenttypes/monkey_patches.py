# monkey patch for collective.portlet.similarcontent
from AccessControl import getSecurityManager, Unauthorized
from Products.CMFCore import permissions
from Products.ZCTextIndex.SetOps import mass_weightedUnion
import math
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

def similar(instance):
    zc = instance.context.portal_catalog
    cat = zc._catalog
    idx = cat.indexes[instance.data.indexname].index
    wordinfo = idx._wordinfo
    docweight = idx._docweight
    num = instance.data.num
    ttc = instance.data.ttc
    N = float(len(docweight))
    meandoclen = idx._totaldoclen() / N
    K1 = idx.K1
    B = idx.B
    K1_plus1 = K1 + 1.0
    B_from1 = 1.0 - B


    # Get the currrent object's path and rid (=docid)
    path = '/'.join(instance.context.getPhysicalPath())
    rid = zc.getrid(path)

    if not rid:
        return []

    # Get all the words in the document
    wids = idx.get_words(rid)

    # Calculate the most 'important' words in this document and
    # we then use those as our query. More efficient than using
    # all words in the document.
    rwids = []
    Wd = docweight[rid]
    lenweight = B_from1 + B * Wd / meandoclen
    for wid in set(wids):
        d2f = wordinfo[wid]
        f = d2f[rid]
        tf = f * K1_plus1 / (f + K1 * lenweight)
        idf = math.log(1.0 + N / float(len(d2f)))
        rwids.append((tf*idf, wid))

    # sort the wids by 'importance' and get the top 20
    rwids.sort()
    rwids.reverse()
    wids = [ wid for (wqt, wid) in rwids[:ttc] ]

    # Do the actual search. We use okapiindex._search_wids here
    # to to the bulk of the work
    res = {}
    rget = res.get
    widres = idx._search_wids(wids)

    # union of all the results
    res = mass_weightedUnion(widres)

    # The max similarity score is the score we get matching ourself...
    maxscore = float(res[rid])
    # ...but we don't want to include ourself
    del res[rid]

    # Sort and un-decorate the document list
    res = [ (score,docid) for (docid,score) in res.items() ]
    res.sort()
    res.reverse()

    similar = []
    count = 0
    types_to_search = set(instance.data.types_to_search)
    # NOTE: now the modification of this monkey patch begins
    security_manager = getSecurityManager()
    for score, docid in res:
        normscore = int((score/maxscore)*100)
        if count > num or normscore < instance.data.cutoff:
            break
        brain = cat[docid]
        try:
            if not security_manager.checkPermission(permissions.View, brain.getObject()):
                continue
        except Unauthorized:
            continue
        if hasattr(instance.context, 'Language') and hasattr(brain, 'Language'):
            if brain.Language!=instance.context.Language():
                continue
        if brain['portal_type'] in types_to_search:
            similar.append(brain)
            count += 1
    # NOTE: now the modification of this monkey patch ends
    return similar

try:
    from collective.portlet.similarcontent.similarcontentportlet import Renderer
    Renderer.original_similar = similar
    Renderer.similar = similar
    Renderer.render = ViewPageTemplateFile('browser/similarcontentportlet.pt')
except ImportError:
    pass
