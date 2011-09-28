from trac.wiki.api import IWikiMacroProvider
from trac.mimeview.api import IHTMLPreviewRenderer
from trac.web.chrome import add_script, ITemplateProvider
from trac.core import *

from genshi.builder import tag
from genshi.core import Markup

MATHJAX_URL = 'https://d3eoax9i5htok0.cloudfront.net/mathjax/latest/MathJax.js'

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

    implements(IHTMLPreviewRenderer, IWikiMacroProvider, ITemplateProvider)

    # IWikiMacroProvider methods

    def get_macros(self):
        yield 'math'

    def get_macro_description(self, name):
        return self.__doc__

    def expand_macro(self, formatter, name, content, args=None):
        add_script(formatter.req, 'mathjax/update.js', 'text/javascript')

        # We access this internals directly because it is not possible to use add_script with full/absolute URL
        # http://trac.edgewall.org/ticket/10369
        # We know scripts and scriptset elements are initialized because we called add_script before
        if MATHJAX_URL not in formatter.req.chrome.get('scriptset'):
            formatter.req.chrome.get('scripts').append({
                'href': MATHJAX_URL + '?delayStartupUntil=configured',
                'type': 'text/javascript',
            })
            formatter.req.chrome.get('scriptset').add(MATHJAX_URL)

        # We load configuration afterwards, as we have delay it with delayStartupUntil and we call MathJax.Hub.Configured here
        # We do this because having text/x-mathjax-config config blocks outside the head does not seem to work
        add_script(formatter.req, 'mathjax/config.js', 'text/javascript')

        if args is None: # Called as macro
            return tag.script(Markup(content), type_="math/tex")
        else: # Called as processor
            return tag.script(Markup(content), type_="math/tex; mode=display")

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
