#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" ITemplateRenderer implementation that uses `Mako`.
"""

__all__ = [
    'MakoTemplateRenderer'
]

import datetime
import utils

from zope.interface import implements
from mako.lookup import TemplateLookup

from interfaces import ITemplateRenderer

DEFAULT_BUILT_INS = {
    "escape": utils.xhtml_escape,
    "url_escape": utils.url_escape,
    "json_encode": utils.json_encode,
    "datetime": datetime
}

class MakoTemplateRenderer(object):
    """ `Mako` template renderer.
    """
    
    implements(ITemplateRenderer)
    
    def __init__(
            self, 
            directories,
            built_ins=None,
            template_lookup_class=None,
            module_directory='/tmp/mako_modules',
            input_encoding='utf-8', 
            output_encoding='utf-8', 
            encoding_errors='replace',
            **kwargs
        ):
        """
        """
        
        self.built_ins = built_ins is None and DEFAULT_BUILT_INS or built_ins
        
        if template_lookup_class is None:
            template_lookup_class = TemplateLookup
        
        self.template_lookup = template_lookup_class(
            directories=directories,
            module_directory=module_directory,
            input_encoding=input_encoding, 
            output_encoding=output_encoding, 
            encoding_errors=encoding_errors,
            **kwargs
        )
        
    
    def render(self, tmpl_name, **kwargs):
        """ Render `tmpl_name`, unpacking `self.built_ins` and `kwargs`
          into the template's global namespace.
        """
        
        params = self.built_ins.copy()
        params.update(kwargs)
        
        t = self.template_lookup.get_template(tmpl_name)
        return t.render(**params)
        
    
    

