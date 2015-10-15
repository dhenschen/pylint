# copyright 2003-2015 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of pylint.
#
# pylint is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option) any
# later version.
#
# pylint is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with pylint.  If not, see <http://www.gnu.org/licenses/>.
"""HTML formatting drivers for ureports"""

from pylint.reporters.ureports import BaseWriter


class HTMLWriter(BaseWriter):
    """format layouts as HTML"""

    def __init__(self, snippet=None):
        super(HTMLWriter, self).__init__()
        self.snippet = snippet

    @staticmethod
    def handle_attrs(layout):
        """get an attribute string from layout member attributes"""
        attrs = u''
        klass = getattr(layout, 'klass', None)
        if klass:
            attrs += u' class="%s"' % klass
        nid = getattr(layout, 'id', None)
        if nid:
            attrs += u' id="%s"' % nid
        return attrs

    def begin_format(self):
        """begin to format a layout"""
        super(HTMLWriter, self).begin_format()
        if self.snippet is None:
            self.writeln(u'<html>')
            self.writeln(u'<body>')

    def end_format(self):
        """finished to format a layout"""
        if self.snippet is None:
            self.writeln(u'</body>')
            self.writeln(u'</html>')

    def visit_section(self, layout):
        """display a section as html, using div + h[section level]"""
        self.section += 1
        self.writeln(u'<div%s>' % self.handle_attrs(layout))
        self.format_children(layout)
        self.writeln(u'</div>')
        self.section -= 1

    def visit_title(self, layout):
        """display a title using <hX>"""
        self.write(u'<h%s%s>' % (self.section, self.handle_attrs(layout)))
        self.format_children(layout)
        self.writeln(u'</h%s>' % self.section)

    def visit_table(self, layout):
        """display a table as html"""
        self.writeln(u'<table%s>' % self.handle_attrs(layout))
        table_content = self.get_table_content(layout)
        for i, row in enumerate(table_content):
            if i == 0 and layout.rheaders:
                self.writeln(u'<tr class="header">')
            elif i+1 == len(table_content) and layout.rrheaders:
                self.writeln(u'<tr class="header">')
            else:
                self.writeln(u'<tr class="%s">' % ('even' if i % 2 else u'odd'))
            for j, cell in enumerate(row):
                cell = cell or u'&#160;'
                if (layout.rheaders and i == 0) or \
                   (layout.cheaders and j == 0) or \
                   (layout.rrheaders and i+1 == len(table_content)) or \
                   (layout.rcheaders and j+1 == len(row)):
                    self.writeln(u'<th>%s</th>' % cell)
                else:
                    self.writeln(u'<td>%s</td>' % cell)
            self.writeln(u'</tr>')
        self.writeln(u'</table>')

    def visit_paragraph(self, layout):
        """display links (using <p>)"""
        self.write(u'<p>')
        self.format_children(layout)
        self.write(u'</p>')

    def visit_verbatimtext(self, layout):
        """display verbatim text (using <pre>)"""
        self.write(u'<pre>')
        self.write(layout.data.replace(u'&', u'&amp;').replace(u'<', u'&lt;'))
        self.write(u'</pre>')

    def visit_text(self, layout):
        """add some text"""
        data = layout.data
        if layout.escaped:
            data = data.replace(u'&', u'&amp;').replace(u'<', u'&lt;')
        self.write(data)