""".. _commands:

==========================================
FogBugz XML API Command Wrappers 
==========================================

Performance Implications
====================================

.. _fborm.commands:

fborm.commands Module Documentation
====================================
"""
from . import objects
from . import parse
from . import util
import re
    
def listFilters(fb, sort_by=None):
    """
    """
    res = fb.listFilters()
    return parse.extract_all(res.filters, objects.fbFilter, {}, sort_by)
    
def setCurrentFilter(fb, filter):
    """
    """
    if isinstance(filter, (int, long)):
        fb.setCurrentFilter(sFilter=str(filter))
    elif isinstance(filter, basestring):
        fb.setCurrentFilter(sFilter=str(filter))
    elif hasattr(filter, has_key) and filter.has_key('sFilter'):
        ## This is a special test that will work with dicts, jsontrees, and
        ## BeautifulSoup elements which are very particular on how you look
        ## up attributes. The 'in' keyword, get, and hasattr have been
        ## overloaded and should be avoided.
        fb.setCurrentFilter(filter['sFilter'])
    else:
        fb.setCurrentFilter(sFilter=filter)

def search(fb, casetype=objects.fbBug,
           q=None,
           namemap={}, sort_by=None, **args):
    """search(fb, casetype=fborm.objects.fbBug, q=None, \
              namemap={}, sort_by=None, **args)
    """
    if 'cols' not in args:
        args['cols'] = parse.keys2cols(casetype, namemap)
    if q is not None:
        args['q'] = q
    res = fb.search(**args)
    cases = parse.extract_all(res.cases, casetype, namemap, sort_by)
    return cases


def new(fb, bug, bugtype, namemap={}, **args):
    if 'cols' in args:
        raise ValueError("You can not specify the 'cols' argument.")
    if bug is None:
        bug = {}
    case = bug
    if args:
        case = dict(bug)
        case.update(args)
    res = fb.new(cols='ixBug', **parse.fbargs(case, bugtype, namemap))
    return parse.extract(res, objects.fbBug_ixBug).ixBug

def _edit(editcall, fb, bug, bugtype, namemap, args):
    cols = args.get('cols', None)
    if cols:
        cols_set = set(util.comma_or_space_split(cols))
        missing = cols_set - set(bugtype.iterkeys())
        if missing:
            raise ValueError(
                "The following 'cols' entries do not have defined types: " +
                ', '.join(missing))
        colstype = dict((cn, bugtype[cn]) for cn in cols_set)
        cols = parse.keys2cols(colstype, namemap)
        args['cols'] = cols
        
    if bug is None:
        bug = {}
    case = bug
    if args:
        case = dict(bug)
        case.update(args)
    res = editcall(**parse.fbargs(case, bugtype, namemap))
    if not cols:
        return None
    return parse.extract(res, colstype, namemap)
    
def edit(fb, bug, bugtype, namemap={}, **args):
    return _edit(fb.edit, fb, bug, bugtype, namemap, args)

def resolve(fb, bug, bugtype, namemap={}, **args):
    return _edit(fb.resolve, fb, bug, bugtype, namemap, args)

def close(fb, bug, bugtype, namemap={}, **args):
    return _edit(fb.close, fb, bug, bugtype, namemap, args)
    
def listTags(fb, tagtype=objects.fbTag, sort_by=None):
    """listTags(fb, tagtype=fborm.objects.fbTag, sort_by=None)
    
    :arg dict tagtype: fborm Api typemap. Defaults to :py:data:`fborm.objects.fbTag`.
    
    """
    return parse.extract_all(fb.listTags().tags, tagtype, {}, sort_by)
    
def viewProject(fb, projecttype=objects.fbProject,
                ixProject=None, sProject=None):
    """viewProject(fb, projecttype=fborm.objects.fbProject, \
                   ixProject=None, sProject=None)
    
    Hello to the documentation.
    
    """
    if (not ixProject and not sProject) or (ixProject and sProject):
        raise ValueError('Must supply ixProject or sProject')
    if ixProject:
        res = fb.viewProject(ixProject=ixProject)
    if sProject:
        res = fb.viewProject(sProject=sProject)
    return parse.extract(res, projecttype)
    
def listProjects(fb, projecttype=objects.fbProject,
                 ixProject=None, fWrite=None, fIncludeDeleted=None,
                 sort_by=('ixProject', 'ixArea')):
    """listProjects(fb, projecttype=fborm.objects.fbProject, \
                    ixProject=None, fWrite=None, fIncludeDeleted=None, \
                    sort_by=('ixProject', 'ixArea'))
    
    
    """
    args = {}
    if ixProject:
        args['ixProject'] = ixProject
    if fWrite:
        args['fWrite'] = 1
    if fIncludeDeleted:
        args['fIncludeDeleted'] = 1
    res = fb.listProjects(**args)
    projects = parse.extract_all(res.projects, projecttype, {}, sort_by)
    return projects

def viewArea(fb, areatype=objects.fbArea,
             ixArea=None, ixProject=None, sArea=None):
    """viewArea(fb, areatype=fborm.objects.fbArea, \
                ixArea=None, ixProject=None, sArea=None)
    """
    if ((not ixArea and (not ixProject or not sArea)) or
        ixArea and (ixProject or sProject)):
        raise ValueError('Must supply ixArea or (ixProject and sArea)')
    if ixArea:
        res = fb.viewArea(ixArea=ixArea)
    else:
        res = fb.viewArea(sArea=sArea, ixProject=ixProject)
    return parse.extract(res, areatype)
    
def listAreas(fb, areatype=objects.fbArea,
              ixProject=None, ixArea=None, fWrite=None,
              sort_by=('ixProject', 'ixArea')):
    """listAreas(fb, areatype=fborm.objects.fbArea, \
                 ixProject=None, ixArea=None, fWrite=None, \
                 sort_by=('ixProject', 'ixArea'))
                 
    """
    args = {}
    if ixProject:
        args['ixProject'] = ixProject
    if ixArea:
        args['ixArea'] = ixArea
    if fWrite:
        args['fWrite'] = 1
    res = fb.listAreas(**args)
    areas = parse.extract_all(res.areas, areatype, {}, sort_by)
    return areas

def viewCategory(fb, ixCategory, categorytype=objects.fbCategory):
    """viewCategory(fb, ixCategory, categorytype=fborm.objects.fbCategory)
    """
    res = fb.viewCategory(ixCategory=ixCategory)
    return parse.extract(res, categorytype)
    
def listCategories(fb, categorytype=objects.fbCategory, sort_by='ixCategory'):
    """listCategories(fb, categorytype=fborm.objects.fbCategory, \
                      sort_by='ixCategory')
    """
    res = fb.listCategories()
    return parse.extract_all(res.categories, categorytype, {}, sort_by)

def viewPriority(fb, ixPriority, prioritytype=objects.fbPriority):
    """viewPriority(fb, ixPriority, prioritytype=fborm.objects.fbPriority)
    """
    res = fb.viewPriority(ixPriority=ixPriority)
    return parse.extract(res, prioritytype)

def listPriorities(fb, prioritytype=objects.fbPriority, sort_by='ixPriority'):
    """listPriorities(fb, prioritytype=fborm.objects.fbPriority, \
                      sort_by='ixPriority')
    """
    res = fb.listPriorities()
    return parse.extract_all(res.priorities, prioritytype, {}, sort_by)

def viewPerson(fb, persontype=objects.fbPerson,
               ixPerson=None, sEmail=None):
    """viewPerson(fb, persontype=fborm.objects.fbPerson, \
                  ixPerson=None, sEmail=None)
    """
    if (not ixPerson and not sEmail) or (ixPerson and sEmail):
        raise ValueError('Must supply ixPerson or sEmail')
    if ixProject:
        res = fb.viewPerson(ixPerson=ixPerson)
    if sProject:
        res = fb.viewPerson(sEmail=sEmail)
    return parse.extract(res, persontype)
    
def listPeople(fb, persontype=objects.fbPerson,
               fIncludeDeleted=None, fIncludeVirtual=None, fIncludeNormal=None,
               fIncludeActive=None, fIncludeCommunity=None, 
               sort_by=None):
    """listPeople(fb, persontype=fborm.objects.fbPerson, \
                  fIncludeDeleted=None, fIncludeVirtual=None, \
                  fIncludeNormal=None, fIncludeActive=None, \
                  fIncludeCommunity=None, sort_by=None)
    
    """
    args = {}
    ## we can not use truth testing because some of these default to 1 in the
    ## api if not supplied. So blanket test to see if it was set away from
    ## None instead of guessing a default that can change on the server.
    if fIncludeDeleted is not None:
        args['fIncludeDeleted'] = int(bool(fIncludeDeleted))
    if fIncludeVirtual is not None:
        args['fIncludeVirtual'] = int(bool(fIncludeVirtual))
    if fIncludeActive is not None:
        args['fIncludeActive'] = int(bool(fIncludeActive))
    if fIncludeCommunity is not None:
        args['fIncludeCommunity'] = int(bool(fIncludeCommunity))
    if fIncludeNormal is not None:
        args['fIncludeNormal'] = int(bool(fIncludeNormal))
    res = fb.listPeople(**args)
    return parse.extract_all(res.people, persontype, {}, sort_by)

def viewStatus(fb, statustype=objects.fbStatus,
               ixStatus=None, ixCategory=None, sStatus=None):
    """viewStatus(fb, statustype=fborm.objects.fbStatus, \
                  ixStatus=None, ixCategory=None, sStatus=None)
    """
    if ((not ixStatus and (not ixCategory or not sStatus)) or
        ixStatus and (ixCategory or sStatus)):
        raise ValueError('Must supply ixStatus or (ixCategory and sStatus)')
    if ixStatus:
        res = fb.viewStatus(ixStatus=ixStatus)
    else:
        res = fb.viewStatus(sStatus=sStatus, ixCategory=ixCategory)
    return parse.extract(res, statustype)
    
def listStatuses(fb, statustype=objects.fbStatus,
                 ixCategory=None, fResolved=None,
                 sort_by=('ixCategory', 'iOrder')):
    """listStatuses(fb, statustype=fborm.objects.fbStatus, \
                    ixCategory=None, fResolved=None, \
                    sort_by=('ixCategory', 'iOrder'))
    """
    args = {}
    if ixCategory:
        args['ixCategory'] = ixCategory
    if fResolved:
        args['fResolved'] = 1
    
    res = fb.listStatuses(**args)
    return parse.extract_all(res.statuses, statustype, {}, sort_by)

def viewFixFor(fb, fixfortype=objects.fbFixFor,
               ixFixFor=None, ixProject=None, sFixFor=None):
    """viewFixFor(fb, fixfortype=fborm.objects.fbFixFor, \
                  ixFixFor=None, ixProject=None, sFixFor=None)
    """
    if ((not ixFixFor and (not ixProject or not sFixFor)) or
        ixFixFor and (ixProject or sFixFor)):
        raise ValueError('Must supply ixFixFor or (ixProject and sFixFor)')
    if ixFixFor:
        res = fb.viewFixFor(ixFixFor=ixFixFor)
    else:
        res = fb.viewFixFor(sFixFor=sFixFor, ixProject=ixProject)
    return parse.extract(res, fixfortype)

def viewMilestone(*args, **kwdargs):
    """viewMilestone(fb, fixfortype=fborm.objects.fbFixFor, \
                     ixFixFor=None, ixProject=None, sFixFor=None)
    alias of :py:func:`fborm.commands.viewFixFor`
    """
    return viewFixFor(*args, **kwdargs)

def listFixFors(fb, fixfortype=objects.fbFixFor,
                ixProject=None, ixFixFor=None, fIncludeDeleted=None,
                fIncludeReallyDeleted=None,
                sort_by='ixProject'):
    """listFixFors(fb, fixfortype=fborm.objects.fbFixFor, \
                   ixProject=None, ixFixFor=None, fIncludeDeleted=None, \
                   fIncludeReallyDeleted=None, \
                   sort_by='ixProject')
    """
    args = {}
    if ixProject:
        args['ixProject'] = ixProject
    if ixFixFor:
        args['ixFixFor'] = ixFixFor
    if fIncludeDeleted:
        args['fIncludeDeleted'] = 1
    if fIncludeReallyDeleted:
        args['fIncludeReallyDeleted'] = 1
        
    res = fb.listFixFors(**args)
    return parse.extract_all(res.fixfors, fixfortype, {}, sort_by)
    
def listMilestones(*args, **kwdargs):
    """listMilestones(fb, fixfortype=fborm.objects.fbFixFor, \
                      ixProject=None, ixFixFor=None, fIncludeDeleted=None, \
                      fIncludeReallyDeleted=None, \
                      sort_by='ixProject'))
    alias of :py:func:`fborm.commands.listFixFors`
    """
    return listFixFors(*args, **kwdargs)


def subscribe(fb, ixBug, ixPerson=None):
    """subscribe(fb, ixBug, ixPerson=None)
    
    To subscribe someone else, you must be logged in as an administrator and
    supply ixPerson.
    """
    if ixPerson is None:
        return fb.subscribe(ixBug=ixBug)
    else:
        return fb.subscribe(ixBug=ixBug, ixPerson=ixPerson)

def unsubscribe(fb, ixBug, ixPerson=None):
    """subscribe(fb, ixBug, ixPerson=None)
    
    To unsubscribe someone else, you must be logged in as an administrator and
    supply ixPerson.
    """
    if ixPerson is None:
        return fb.unsubscribe(ixBug=ixBug)
    else:
        return fb.unsubscribe(ixBug=ixBug, ixPerson=ixPerson)
        