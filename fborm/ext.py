""".. _extensions:

==========================================
Extensions to the FogBugz XML API
==========================================

.. _fborm.ext:

fborm.ext Module Documentation
====================================
"""
from . import objects
from . import commands
import re

_customfields_re = re.compile("^plugin_customfields.*")

def listCustomFieldNames(fb, sample_bugs='1,2,3'):
    """
    """
    customs = fb.search(q=sample_bugs, cols='plugin_customfields', max=1)
    found = set(ent.name for ent in customs.findAll(_customfields_re))
    found.remove('plugin_customfields')
    return sorted(found)
    
def listAllPeople(fb, persontype=objects.fbPerson, sort_by=None):
    """listAllPeople(fb, persontype=fborm.objects.fbPerson, sort_by=None)
    """
    return commands.listPeople(
        fb, persontype=persontype, sort_by=sort_by,
        fIncludeDeleted=1, fIncludeVirtual=1, fIncludeNormal=1,
        fIncludeActive=1, fIncludeCommunity=1)
    