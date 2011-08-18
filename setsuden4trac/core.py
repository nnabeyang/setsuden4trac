from trac.core import *
from trac.timeline.api import ITimelineEventProvider
from trac.admin import *
from genshi.builder import tag
from datetime import datetime
from trac.util.translation import _, tag_
from setsuden4trac.reader import Reader
from trac.util.datefmt import format_time
from trac.web.chrome import add_stylesheet, ITemplateProvider
from pkg_resources import resource_filename

import sys
class GoSetsudenComponent(Component):
    implements(ITimelineEventProvider,IAdminCommandProvider, ITemplateProvider)
    def __init__(self):
        self.reader = None
    def set_reader(self):
        if self.reader is None:
            region = self.env.config.get('setsuden', 'region') or 'kansai'
            self.reader = Reader(region)
    # ITemplateProvider methods
    def get_htdocs_dirs(self):
         return [('setsuden4trac', resource_filename('setsuden4trac', 'htdocs'))]
    def get_templates_dirs(self):
        pass
    # ITimelineEventProvider methods
    def get_timeline_filters(self, req):
        yield ('gosetsuden', _('gosetsuden'))
    def get_timeline_events(self, req, start, stop, filters):
        self.set_reader()
        result = self.reader.getusage()
        usage = result['usage']
        class_name = ''
        if usage < 90:
            class_name = 'gosetsuden_green'
        elif usage < 95:
            class_name = 'gosetsuden_yellow'
        else:
            class_name = 'gosetsuden_red'

        desc = "usage %d%%" % usage
        add_stylesheet(req, "setsuden4trac/css/setsuden.css")
        yield (class_name, result['datetime'], self.reader.author(), ('http://www.gosetsuden.jp/', desc))
    def render_timeline_event(self, context, field, event):
        url, desc = event[3]
        if field == 'url':
            return url
        elif field == 'title':
            return tag_('%(page)s created', page=tag.em('SETSUDEN'))
        elif field == 'description':
            return tag(desc)
    # IAdminCommdandProvider methods
    def get_admin_commands(self):
        yield ("setsuden usage", "", "setsuden", None, self._say_hello)
    def _say_hello(self):
        self.set_reader()
        result = self.reader.getusage()
        desc = "%s usage %d%% @%s" % (format_time(result['datetime'], str('%H:%M')), result['usage'], self.reader.region)
        print desc
