""".. _objects:

==========================================
Object Type Mappings
==========================================

Performance Implications
====================================

.. fborm.objects:

fborm.objects Module Documentation
====================================
"""
from . import types
from . import parse

#:
fbError = dict(
    sError          = types.fbself,
    code            = types.fbattr(types.fbint)
)

#:
fbFilter = dict(
    sFilterName     = types.fbself,
    type            = types.fbattr(types.fbstring),
    sFilter         = types.fbattr(types.fbstring),
    status          = types.fbattr(types.fbstring))
"""
:kvp sFilterName: Name of the filer which is dsiplayed in the UI.
:kvp fborm.types.fbattr type: Attribute of type :py:data:`fborm.types.fbstring` which will have the value of ``"builtin"``, ``"saved"``, or ``"shared"``.
:kvp fborm.types.fbattr sFilter: Attribute of type :py:data:`fborm.types.fbstring` which may either be the name of one of the special built-in filters or it will be the filter id seen in the URL. This is the value to use with the :py:func:`fborm.commands.setCurrentFilter` command.
:kvp fborm.types.fbattr status: Attribute of type :py:data:`fborm.types.fbstring` which will have the value of ``"current"`` or it will be ``None``.

The FogBugz API call listFilters has output that is different from all the
other API calls. The data returned is not parameterized into tags. Instead
the data that is useful are attributes on teh parent tag. This means we need
to do some special processing to extract the data in a meaningful way.
Here is an example return by the API:

.. code:: xml

    <filters>
        <filter type="builtin" sFilter="ez">My Cases</filter>
        <filter type="builtin" sFilter="inbox">Inbox</filter>
        <filter type="shared" sFilter="7"><![CDATA[Active Bugs Outline]]></filter>
        <filter type="shared" sFilter="9"><![CDATA[Active Requests Outline]]></filter>
        <filter type="shared" sFilter="13"><![CDATA[All Active]]></filter>
    </filters>

The XML attribute **sFilter** is what needs to be passed as an argument to
The FogBugz API call ``setCurrentFilter``. To simplify and make the API uniform
the FogBugz-ORM wrapper API converts this into a standardized structure.
The FogBugz ORM wrapper API call :py:func:`fborm.commands.setCurrentFilter`
has also been extended to support a number of inputs, including this structure.

See :py:func:`fborm.commands.listFilters` ,
:py:func:`fborm.commands.setCurrentFilter` and
`FogBugz API - Filters`_ for more information.

.. _FogBugz API - Filters: http://fogbugz.stackexchange.com/fogbugz-xml-api#filters

"""
#:
fbTag = dict(
    ixTag       = types.fbint,
    sTag        = types.fbstring,
    cTagUses    = types.fbint)

#:
fbPerson = dict(
    ixPerson        = types.fbint,
    sFullName       = types.fbstring,
    sEmail          = types.fbstring,
    sPhone          = types.fbstring,
    fAdministrator  = types.fbbool,
    fCommunity      = types.fbbool,
    fVirtual        = types.fbbool,
    fDeleted        = types.fbbool,
    fNotify         = types.fbbool,
    sHomepage       = types.fbstring,
    sLocale         = types.fbstring,
    sLanguage       = types.fbstring,
    sTimeZoneKey    = types.fbstring,
    sLDAPUid        = types.fbstring,
    dtLastActivity  = types.fbdatetime,
    fRecurseBugChildren = types.fbbool,
    fPaletteExpanded    = types.fbbool,
    ixBugWorkingOn  = types.fbint,
    sFrom           = types.fbstring)

#:
fbProject = dict(
    ixProject       = types.fbint,
    sProject        = types.fbstring,
    ixPersonOwner   = types.fbint,
    sPersonOwner    = types.fbstring,
    sEmail          = types.fbstring,
    sPhone          = types.fbstring,
    fInbox          = types.fbbool,
    ixWorkflow      = types.fbint,
    fDeleted        = types.fbbool)

#:
fbCategory = dict(
    ixCategory      = types.fbint,
    sCategory       = types.fbstring,
    sPlural         = types.fbstring,
    ixStatusDefault = types.fbint,
    fIsScheduleItem = types.fbbool,
    fDeleted        = types.fbbool,
    iOrder          = types.fbint,
    nIconType       = types.fbint,
    ixAttachmentIcon    = types.fbint,
    ixStatusDefaultActive   = types.fbint)

#:
fbPriority = dict(
    ixCategory      = types.fbint,
    fDefault        = types.fbbool,
    sPriority       = types.fbstring)

#:
fbStatus = dict(
    ixStatus        = types.fbint,
    sStatus         = types.fbstring,
    ixCategory      = types.fbint,
    fWorkDone       = types.fbbool,
    fResolved       = types.fbbool,
    fDuplicate      = types.fbbool,
    fDeleted        = types.fbbool,
    iOrder          = types.fbint)

#:
fbArea = dict(
    ixArea          = types.fbint,
    sArea           = types.fbstring,
    ixProject       = types.fbint,
    sProject        = types.fbstring,
    ixPersonOwner   = types.fbint,
    sPersonOwner    = types.fbstring,
    nType           = types.fbint,
    cDoc            = types.fbint)

#:
fbAttachment = dict(
    sFilename       = types.fbstring,
    sURL            = types.fbstring)

#:
fbstring_fEmail = types.fbconditional(
    types.fbstring, fEmail=lambda fEmail: fEmail)

#:
fbBugMiniEvent = dict(
    ixBugEvent      = types.fbint,
    ixBug           = types.fbattr(types.fbint),
    evt             = types.fbint,
    sVerb           = types.fbstring,
    ixPerson        = types.fbint,
    sPerson         = types.fbstring,
    ixPersonAssignedTo = types.fbint,
    dt              = types.fbdatetime,
    fHTML           = types.fbbool,
    sFormat         = types.fbstring,
    sChanges        = types.fbstring,
    evtDescription  = types.fbstring,
    rgAttachments   = types.fblistof(fbAttachment),
    fEmail          = types.fbbool,
    fExternal       = types.fbbool,
    
    ## Thse are only set when fEmail is true,
    ## otherwise omitted from return data
    sFrom           = fbstring_fEmail,
    sTo             = fbstring_fEmail,
    sBCC            = fbstring_fEmail,
    sReplyTo        = fbstring_fEmail,
    sSubject        = fbstring_fEmail,
    sDate           = fbstring_fEmail,
    sBody           = fbstring_fEmail,
    sBodyHTML       = fbstring_fEmail)

#:
fbBugEvent = dict(
    s               = types.fbstring,
    sHTML           = types.fbstring,
    **fbBugMiniEvent)

#: very common for use with adding a new case
fbBug_ixBug = dict(
    ixBug           = types.fbint)

#:
fbBug = dict(
    ixBug           = types.fbint,
    ixBugParent     = types.fbint,
    ixBugChildren   = types.fbixBugChildren,
    sTitle          = types.fbstring,
    ixProject       = types.fbint,
    sProject        = types.fbstring,
    ixArea          = types.fbint,
    sArea           = types.fbstring,
    ixCategory      = types.fbint,
    sCategory       = types.fbstring,
    ixPriority      = types.fbint,
    sPriority       = types.fbstring,
    ixPersonAssignedTo = types.fbint,
    sPersonAssignedTo  = types.fbstring)

#:
fbBug_withLatestEvent = dict(
    latestEvent     = types.fblatestevent(fbBugEvent),
    **fbBug)

#:
fbBug_withEvents = dict(
    events          = types.fbevents(fbBugEvent),
    **fbBug)

#:
fbBug_withMiniEvents = dict(
    minievents      = types.fbminievents(fbBugMiniEvent),
    **fbBug)

#:
fbFixFor = dict(
    ixFixFor        = types.fbint,
    sFixFor         = types.fbstring,
    ixProject       = types.fbint,
    sProject        = types.fbstring,
    fDeleted        = types.fbcol(types.fbbool, setname='fAssignable'),
    fReallyDeleted  = types.fbbool,
    dt              = types.fbcol(types.fbdatetime, setname='dtRelease'),
    dtStart         = types.fbdatetime,
    sStartNote      = types.fbstring,
    setixForForDependency = types.fbcol(types.fblistof(types.fbint),
                                        settable=False))



#: alias of :py:data:`fborm.objects.fbFixFor`
fbMilestone = fbFixFor
