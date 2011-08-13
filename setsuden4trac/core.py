from trac.core import *
from trac.timeline.api import ITimelineEventProvider
from trac.admin import *
from genshi.builder import tag
from datetime import datetime
from trac.util.datefmt import utc
from trac.util.translation import _, tag_
from setsuden4trac.reader import Reader
import sys
class GoSetsudenComponent(Component):
    implements(ITimelineEventProvider,IAdminCommandProvider)
    def __init__(self):
        self.reader = Reader('kansai')
    # ITimelineEventProvider methods
    def get_timeline_filters(self, req):
        yield ('gosetsuden', _('gosetsuden opened'))
    def get_timeline_events(self, req, start, stop, filters):
        result = self.reader.getusage()
        desc = "%d%%use" % result['usage']
        yield ('gosetsuden', datetime.now(utc), self.reader.author(), ('http://www.gosetsuden.jp/', desc))
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
        result = self.reader.getusage()
        desc = "%d%%use @%s" % (result['usage'], self.reader.region)
        print desc
