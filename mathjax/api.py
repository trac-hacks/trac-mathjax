from trac.wiki.api import IWikiMacroProvider
from trac.mimeview.api import IHTMLPreviewRenderer
from trac.web.api import ITemplateStreamFilter
from trac.core import *

from genshi.builder import tag
from genshi.core import Markup
from genshi.filters.transform import Transformer

MATHJAX_CONFIGURATION = """
MathJax.Hub.Config({'tex2jax': {
  'inlineMath': [],
  'displayMath': [],
  'processEnvironments': false
}});
"""

class MathJax(Component):
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

    implements(IHTMLPreviewRenderer, IWikiMacroProvider, ITemplateStreamFilter)

    # IWikiMacroProvider methods

    def get_macros(self):
        yield 'math'

    def get_macro_description(self, name):
        return self.__doc__

    def expand_macro(self, formatter, name, content, args=None):
        if args is None: # Called as macro
            return tag.script(Markup(content), type_="math/tex")
        else: # Called as processor
            return tag.script(Markup(content), type_="math/tex; mode=display")

    # IHTMLPreviewRenderer methods

    def get_quality_ratio(self, mimetype):
        if mimetype in ('text/x-mathjax',):
            return 2
        return 0

    # ITemplateStreamFilter methods

    def filter_stream(self, req, method, filename, stream, data):
        return stream | Transformer('head').append(
            tag.script(MATHJAX_CONFIGURATION, type_="text/javascript")
        ).append(
            tag.script(
                type_="text/javascript",
                src="https://d3eoax9i5htok0.cloudfront.net/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"
            )
        )
