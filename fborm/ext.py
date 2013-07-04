""".. _extensions:

==========================================
Extensions to the FogBugz XML API
==========================================

.. _fborm.ext:

fborm.ext Module Documentation
====================================
"""

import re

_customfields_re = re.compile("^plugin_customfields.*")

def listCustomFieldNames(fb, sample_bugs='1,2,3'):
    customs = fb.search(q=sample_bugs, cols='plugin_customfields', max=1)
    found = set(ent.name for ent in customs.findAll(_customfields_re))
    found.remove('plugin_customfields')
    return sorted(found)
    
    