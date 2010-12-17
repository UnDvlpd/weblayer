#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Helper class to simplify bootstrapping the application
  using imperative configuration.
"""

import venusian

from component import registry
from interfaces import *

from auth import TrivialAuthenticationManager
from cookie import SignedSecureCookieWrapper
from method import ExposedMethodSelector
from normalise import DefaultToJSONResponseNormaliser
from route import RegExpPathRouter
from settings import require_setting, RequirableSettings
from template import MakoTemplateRenderer

class Bootstrapper(object):
    """
    """
    
    def scan(
            self, 
            packages=None, 
            extra_categories=None, 
            scan_defaults=True
            settings=None
        ):
        """ Run a `venusian` scan on packages.  Include `thruflo.webapp` 
          and the calling module or module's package by default.
        """
        
        if settings is None:
            scanner = venusian.Scanner(settings=self._settings)
        else:
            scanner = venusian.Scanner(settings=settings)
        
        categories = ['thruflo']
        if extra_categories is not None:
            for item in extra_categories:
                categories.append(item)
        
        if scan_defaults:
            import thruflo.webapp
            scanner.scan(thruflo.webapp, categories=categories)
            # @@ get the calling module / module's package
            # scanner.scan(caller, categories=categories)
            raise NotImplementedError
        
        if packages is not None:
            for item in packages:
                scanner.scan(item, categories=categories)
            
        return scanner
        
    
    def setup_components(
            self, 
            path_router=None,
            settings=None,
            template_renderer=None,
            AuthenticationManager=None, 
            SecureCookieWrapper=None, 
            MethodSelector=None,
            ResponseNormaliser=None
        ):
        """ Setup component registrations. Pass in alternative implementations
          here to override (or simply register overrides later).
        """
        
        if path_router is not False:
            if path_router is None:
                path_router = RegExpPathRouter(self._url_mapping)
            registry.registerUtility(path_router, IPathRouter)
        
        if settings is not False:
            if settings is None:
                settings = self._settings(self._user_settings)
            registry.registerUtility(settings, ISettings)
        
        if template_renderer is not False:
            if template_renderer is None:
                template_renderer = MakoTemplateRenderer()
            registry.registerUtility(template_renderer, ITemplateRenderer)
        
        if AuthenticationManager is not False:
            if AuthenticationManager is None:
                AuthenticationManager = TrivialAuthenticationManager
            registry.registerAdapter(
                AuthenticationManager, 
                adapts=[IRequestHandler],
                provides=IAuthenticationManager
            )
        
        if SecureCookieWrapper is not False:
            if SecureCookieWrapper is None:
                SecureCookieWrapper = SignedSecureCookieWrapper
            registry.registerAdapter(
                SecureCookieWrapper, 
                adapts=[IRequestHandler],
                provides=ISecureCookieWrapper
            )
        
        if MethodSelector is not False:
            if MethodSelector is None:
                MethodSelector = ExposedMethodSelector
            registry.registerAdapter(
                MethodSelector, 
                adapts=[IRequestHandler],
                provides=IMethodSelector
            )
        
        if ResponseNormaliser is not False:
            if ResponseNormaliser is None:
                ResponseNormaliser = DefaultToJSONResponseNormaliser
            registry.registerAdapter(
                ResponseNormaliser, 
                adapts=[IResponse],
                provides=IResponseNormaliser
            )
        
    
    
    def __init__(self, settings={}, url_mapping=[], template_directories):
        """
        """
        
        self._user_settings = settings
        self._url_mapping = url_mapping
        
        self._settings = RequirableSettings()
        
    
    


