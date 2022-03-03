
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2024 Mitar <mitar.trac@tnode.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

from trac.core import *
from trac.mimeview.api import IHTMLPreviewRenderer
from trac.util.html import Markup, html as tag
from trac.web.chrome import ITemplateProvider, add_script
from trac.wiki.api import IWikiMacroProvider
from trac.wiki import IWikiSyntaxProvider

MATHJAX_URL = 'mathjax/MathJax/MathJax.js'
# Install MathJax 2.7.9 locally:
# wget https://github.com/mathjax/MathJax/archive/3b461438246adfcf67690795fcc0ae6dc4e335fe.zip
# unpack into TracMathJax-0.1.7-py2.7.egg/mathjax/htdocs/MathJax
# restart server

class MathJaxPlugin(Component):
    """Renders mathematical equations using MathJax library.

    Examples:

    {{{
        [[math(1+2=3)]]
        {{{
        #!math
        x = \frac{1}{2}
        }}}
    }}}
    """
    implements(IHTMLPreviewRenderer, ITemplateProvider, IWikiMacroProvider, IWikiSyntaxProvider)

    # IWikiMacroProvider methods

    def get_macros(self):
        return ('latex', 'Latex', 'LaTeX', 'math')
        #yield 'math'

    def get_macro_description(self, name):
        return self.__doc__

    def expand_macro(self, formatter, name, content, args=None):
        req = formatter.req

        if add_script(req, MATHJAX_URL) is not False:
            # We access this internals directly because it is not possible to
            # use add_script with full/absolute URL (trac:#10369).
            req.chrome.get('scripts')[-1]['href'] = \
                MATHJAX_URL + '?delayStartupUntil=onload'
            # We load configuration afterwards, as we have delay it with
            # delayStartupUntil and we call MathJax.Hub.Configured here. We do
            # this because having text/x-mathjax-config config blocks outside
            # the head does not seem to work.
            add_script(req, 'mathjax/config.js', 'text/javascript')
            add_script(req, 'mathjax/update.js', 'text/javascript')

        # It is unable to avoid script injection via <script type="math/tex">
        # with the given text. Instead, we create the same script tag using
        # javascript on document's ready.
        if args is None:  # Called as macro
            element = tag.span
        else:  # Called as processor
            element = tag.div
        return Markup(element(content, class_='trac-mathjax',
                             style='display:none'))

    # IHTMLPreviewRenderer methods

    def get_quality_ratio(self, mimetype):
        if mimetype in ('text/x-mathjax',):
            return 2
        return 0

    # ITemplateProvider methods

    def get_templates_dirs(self):
        return []

    def get_htdocs_dirs(self):
        from pkg_resources import resource_filename
        return [('mathjax', resource_filename(__name__, 'htdocs'))]

    # IWikiSyntaxProvider methos

    def get_link_resolvers(self):
        return

    def get_wiki_syntax(self):
        yield (r"(?P<delim>\\\(|\$\$|\\\[)(?P<math>.*?)(\\\)|\$\$|\\\])", self._format_regex_math)

    def _format_regex_math(self, formatter, ns, match):
        self.env.log.debug('formatter: %s ns: %s' % (formatter, ns))
        maths = match.group('math')
        delim = match.group('delim')
        if delim == "\(":
            argg = None
        else:
            argg = { 'delim': delim }
        return self.expand_macro(formatter, ns, maths, argg )
