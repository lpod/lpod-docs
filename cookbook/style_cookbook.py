# -*- coding: UTF-8 -*-
#
# Copyright (c) 2009 Ars Aperta, Itaapy, Pierlis, Talend.
#
# Authors: Hervé Cauwelier <herve@itaapy.com>
#
# This file is part of Lpod (see: http://lpod-project.org).
# Lpod is free software; you can redistribute it and/or modify it under
# the terms of either:
#
# a) the GNU General Public License as published by the Free Software
#    Foundation, either version 3 of the License, or (at your option)
#    any later version.
#    Lpod is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    You should have received a copy of the GNU General Public License
#    along with Lpod.  If not, see <http://www.gnu.org/licenses/>.
#
# b) the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
#

# Import from Standard Library
from datetime import date
from os.path import normpath, join

# Import from lpod
import lpod
from lpod.document import odf_get_document, odf_new_document_from_type
from lpod.paragraph import odf_create_paragraph
from lpod.style import odf_create_style, odf_create_default_date_style
from lpod.variable import odf_create_date_variable

# Creation of the document
document = odf_new_document_from_type('text')
body = document.get_body()

#
# use merge_styles_from to copy default style from some document
#
path = normpath(join(lpod.__file__, '../templates/lpod_styles.odt'))
doc_style = odf_get_document(path)
document.merge_styles_from(doc_style)

#
# Pages, header and footer
#

# Automatic style to set the master page
style = odf_create_style('paragraph', master_page=u"First_20_Page")
document.insert_style(style, automatic=True)

# The first paragraph will set the page::
paragraph = odf_create_paragraph(text=u"lpOD generated Document "
        u"with styled pages", style=style.get_style_name())
body.append(paragraph)

# To modify the footer and header we get the style
first_page_style = document.get_style('master-page', u"First_20_Page")

# Overwrite the footer
first_page_style.set_footer(u'lpOD project')

# Complement the header
header = first_page_style.get_header()
header.append(odf_create_paragraph(u"Final Version"))

# Example of default style: a date
date_style = odf_create_default_date_style()
document.insert_style(date_style, automatic=True)
today = odf_create_date_variable(date.today(),
                                 data_style=date_style.get_style_name())
paragraph = odf_create_paragraph(
                text=u"The current date with the default lpOD date style: ")
paragraph.append(today)
body.append(paragraph)


# Save
filename = 'styles.odt'
document.save(filename, pretty=True)
print 'Document "%s" generated.' % filename
