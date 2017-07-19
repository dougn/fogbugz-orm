"""
=============================================
FogBugzORM Extended Interface
=============================================


fborm Module Documentation
===========================
"""

__version__ = (0,3,3)
__version_string__ = '.'.join(str(x) for x in __version__)

__author__ = 'Doug Napoleone'
__email__ = 'doug.napoleone+fborm@gmail.com'

from .util import *
from .types import *
from .objects import *
from .parse import *
from .commands import *
from .ext import *

class FogBugzORM:
    """FogBugzORM Class Interface Documentation
    
    
    """
    
    #########################################################################
    ## Initialization and Authentication
    
    def __init__(self, hostname, token=None, username=None, password=None,
                 namemap={}):
        if token and (username or password):
            raise TypeError(
                "if you supply 'token' you can"
                "not supply 'username' or 'password'")
        if (username and not password) or (not username and password):
            raise TypeError(
                "You must supply both 'username' and 'password'")
        self.namemap = namemap
        import fogbugz
        self.fb = fogbugz.FogBugz(hostname, token=token)
        self.username = username
        self.password = password
        if username:
            self.fb.logon(username, password)
    
    def logon(self, username=None, password=None, logoff=True):
        """
        """
        if not username and not self.username:
            raise TypeError("must supply 'username'")
        if not password and not self.password:
            raise TypeError("must supply 'password'")
        if username:
            self.username = username
        if password:
            self.password = password
        if logoff and self.token:
            self.logoff()
        self.fb.logon(self.username, self.password)
    
    def loggedon(self):
        return bool(self.token)
        
    def logoff(self):
        """
        """
        if self.fb._token:
            self.fb.logoff()
            self.fb._token=None
        
    @property
    def token(self):
        return self.fb._token
    
    @token.setter
    def token(self, token):
        return self.fb.token(token)
        
    def __enter__(self):
        return self
    
    def __exit__(self, *args, **kwdargs):
        try:
            self.logoff()
        except:
            pass
    
    def generate_token(self, username=None, password=None):
        """
        """
        if not username and not self.username:
            raise TypeError("must supply 'username'")
        if not password and not self.password:
            raise TypeError("must supply 'password'")
        if not username:
            username = self.username
        if not password:
            password = self.password
        
        old_token = self.fb._token
        token = None
        try:
            self.fb.logon(username, password)
            token = self.fb._token
        finally:
            self.fb._token = old_token
        return token
    
    def release_token(self, token):
        """
        """
        old_token = self.fb._token
        self.fb._token = token
        try:
            self.fb.logoff()
        finally:
            self.fb._token = old_token
    
    #########################################################################
    ## Extension interfaces, that look like API, but are not
    
    def listCustomFieldNames(self, sample_bugs='1,2,3'):
        """Wrapper around :py:func:`fborm.ext.listCustomFieldNames` .
        The first argument, the fogbugz instance, is supplied automatically.
        """
        return listCustomFieldNames(self.fb, sample_bugs)
    
    def listAllPeople(self, *args, **kwdargs):
        """Wrapper around :py:func:`fborm.ext.listAllPeople` .
        The first argument, the fogbugz instance, is supplied automatically.
        """
        return listAllPeople(self.fb, *args, **kwdargs)
        
    #########################################################################
    ## Now we get to the standard interfaces
    
    def listFilters(self, sort_by=None):
        """Wrapper around :py:func:`fborm.commands.listFilters` .
        The first argument, the fogbugz instance, is supplied automatically.
        """
        return listFilters(self.fb, sort_by=sort_by)
        
    def setCurrentFilter(self, filter):
        """Wrapper around :py:func:`fborm.commands.setCurrentFilter` .
        The first argument, the fogbugz instance, is supplied automatically.
        
        This extends the normal inerface to accept multiple types of objects
        for the **filter** argument.
        """
        return setCurrentFilter(self.fb, filter)
        
    def search(self, *args, **kwdargs):
        """Wrapper around :py:func:`fborm.commands.search` .
        The first argument, the fogbugz instance, is supplied automatically.
        The keyword argument **namemap**, if not supplied, will be set to
        the the namemap member supplied durring construction.
        """
        if 'namemap' not in kwdargs:
            kwdargs = dict(kwdargs)
            kwdargs['namemap'] = self.namemap
        return search(self.fb, *args, **kwdargs)

    def new(self, bug, bugtype, **kwdargs):
        """Wrapper around :py:func:`fborm.commands.new` .
        The first argument, the fogbugz instance, is supplied automatically.
        The keyword argument **namemap**, if not supplied, will be set to
        the the namemap member supplied durring construction.
        """
        if 'namemap' not in kwdargs:
            kwdargs = dict(kwdargs)
            kwdargs['namemap'] = self.namemap
        return new(self.fb, bug, bugtype, **kwdargs)
        
    def edit(self, bug, bugtype, **kwdargs):
        """Wrapper around :py:func:`fborm.commands.edit` .
        The first argument, the fogbugz instance, is supplied automatically.
        The keyword argument **namemap**, if not supplied, will be set to
        the the namemap member supplied durring construction.
        """
        if 'namemap' not in kwdargs:
            kwdargs = dict(kwdargs)
            kwdargs['namemap'] = self.namemap
        return edit(self.fb, bug, bugtype, **kwdargs)
        
    def resolve(self, bug, bugtype, **kwdargs):
        """Wrapper around :py:func:`fborm.commands.resolve` .
        The first argument, the fogbugz instance, is supplied automatically.
        The keyword argument **namemap**, if not supplied, will be set to
        the the namemap member supplied durring construction.
        """
        if 'namemap' not in kwdargs:
            kwdargs = dict(kwdargs)
            kwdargs['namemap'] = self.namemap
        return resolve(self.fb, bug, bugtype, **kwdargs)
        
    def close(self, bug, bugtype, **kwdargs):
        """Wrapper around :py:func:`fborm.commands.resolve` .
        The first argument, the fogbugz instance, is supplied automatically.
        The keyword argument **namemap**, if not supplied, will be set to
        the the namemap member supplied durring construction.
        """
        if 'namemap' not in kwdargs:
            kwdargs = dict(kwdargs)
            kwdargs['namemap'] = self.namemap
        return close(self.fb, bug, bugtype, **kwdargs)
        
    def listTags(self, *args, **kwdargs):
        """Wrapper around :py:func:`fborm.commands.listTags` .
        The first argument, the fogbugz instance, is supplied automatically.
        """
        return listTags(self.fb, *args, **kwdargs)
    
    def viewProject(self, *args, **kwdargs):
        """Wrapper around :py:func:`fborm.commands.viewProject` .
        The first argument, the fogbugz instance, is supplied automatically.
        """
        return viewProject(self.fb, *args, **kwdargs)
        
    def listProjects(self, *args, **kwdargs):
        """Wrapper around :py:func:`fborm.commands.listProjects` .
        The first argument, the fogbugz instance, is supplied automatically.
        """
        return listProjects(self.fb, *args, **kwdargs)
        
    def viewArea(self, *args, **kwdargs):
        """Wrapper around :py:func:`fborm.commands.viewArea` .
        The first argument, the fogbugz instance, is supplied automatically.
        """
        return viewArea(self.fb, *args, **kwdargs)
        
    def listAreas(self, *args, **kwdargs):
        """Wrapper around :py:func:`fborm.commands.listAreas` .
        The first argument, the fogbugz instance, is supplied automatically.
        """
        return listAreas(self.fb, *args, **kwdargs)
        
    def viewCategory(self, *args, **kwdargs):
        """Wrapper around :py:func:`fborm.commands.viewCategory` .
        The first argument, the fogbugz instance, is supplied automatically.
        """
        return viewCategory(self.fb, *args, **kwdargs)
        
    def listCategories(self, *args, **kwdargs):
        """Wrapper around :py:func:`fborm.commands.listCategories` .
        The first argument, the fogbugz instance, is supplied automatically.
        """
        return listCategories(self.fb, *args, **kwdargs)
        
    def viewPriority(self, *args, **kwdargs):
        """Wrapper around :py:func:`fborm.commands.viewPriority` .
        The first argument, the fogbugz instance, is supplied automatically.
        """
        return viewPriority(self.fb, *args, **kwdargs)
        
    def listPriorities(self, *args, **kwdargs):
        """Wrapper around :py:func:`fborm.commands.listPriorities` .
        The first argument, the fogbugz instance, is supplied automatically.
        """
        return listPriorities(self.fb, *args, **kwdargs)
        
    def viewPerson(self, *args, **kwdargs):
        """Wrapper around :py:func:`fborm.commands.viewPerson` .
        The first argument, the fogbugz instance, is supplied automatically.
        """
        return viewPerson(self.fb, *args, **kwdargs)
        
    def listPeople(self, *args, **kwdargs):
        """Wrapper around :py:func:`fborm.commands.listPeople` .
        The first argument, the fogbugz instance, is supplied automatically.
        """
        return listPeople(self.fb, *args, **kwdargs)
        
    def viewStatus(self, *args, **kwdargs):
        """Wrapper around :py:func:`fborm.commands.viewStatus` .
        The first argument, the fogbugz instance, is supplied automatically.
        """
        return viewStatus(self.fb, *args, **kwdargs)
        
    def listStatuses(self, *args, **kwdargs):
        """Wrapper around :py:func:`fborm.commands.listStatuses` .
        The first argument, the fogbugz instance, is supplied automatically.
        """
        return listStatuses(self.fb, *args, **kwdargs)
        
    def viewFixFor(self, *args, **kwdargs):
        """Wrapper around :py:func:`fborm.commands.viewFixFor` .
        The first argument, the fogbugz instance, is supplied automatically.
        """
        return viewFixFor(self.fb, *args, **kwdargs)
        
    def viewMilestone(self, *args, **kwdargs):
        """Wrapper around :py:func:`fborm.commands.viewMilestone` which
        is an alias for :py:func:`fborm.commands.viewFixFor` .
        The first argument, the fogbugz instance, is supplied automatically.
        """
        return viewMilestone(self.fb, *args, **kwdargs)
        
    def listFixFors(self, *args, **kwdargs):
        """Wrapper around :py:func:`fborm.commands.listFixFors` .
        The first argument, the fogbugz instance, is supplied automatically.
        """
        return listFixFors(self.fb, *args, **kwdargs)
        
    def listMilestones(self, *args, **kwdargs):
        """Wrapper around :py:func:`fborm.commands.listMilestones` which
        is an alias for :py:func:`fborm.commands.listFixFors` .
        The first argument, the fogbugz instance, is supplied automatically.
        """
        return listMilestones(self.fb, *args, **kwdargs)
        
    def subscribe(self, ixBug, ixPerson=None):
        """Wrapper around :py:func:`fborm.commands.subscribe` .
        The first argument, the fogbugz instance, is supplied automatically.
        """
        return subscribe(self.fb, ixBug, ixPerson)
    
    def unsubscribe(self, ixBug, ixPerson=None):
        """Wrapper around :py:func:`fborm.commands.unsubscribe` .
        The first argument, the fogbugz instance, is supplied automatically.
        """
        return unsubscribe(self.fb, ixBug, ixPerson)
        