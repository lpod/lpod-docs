# -*- coding: UTF-8 -*-
# Copyright (C) 2009 Itaapy, ArsAperta, Pierlis, Talend

# Import from the Standard Library
import unittest
from unittest import TestCase

# Import from lpod
from lpod.container import new_odf_container, get_odf_container
from lpod.container import ODF_EXTENSIONS


class NewContainerTestCase(TestCase):

    def test_no_parameters(self):
        self.assertRaises(ValueError, new_odf_container)


    def test_bad_class(self):
        self.assertRaises(ValueError, new_odf_container, odf_class='foobar')


    def test_all_parameters(self):
        self.assertRaises(ValueError, new_odf_container, odf_class='text',
                          template_uri='templates/text.ott')


    def test_text_template(self):
        new_odf_container(odf_class='text')


    def test_spreadsheet_template(self):
        new_odf_container(odf_class='spreadsheet')


    def test_presentation_template(self):
        new_odf_container(odf_class='presentation')


    def test_drawing_template(self):
        new_odf_container(odf_class='drawing')



class GetContainerTestCase(TestCase):

    def test_filesystem(self):
        path = 'samples/example.odt'
        container = get_odf_container(path)


    def test_http(self):
        uri = 'http://test.lpod-project.org/example.odt'
        container = get_odf_container(uri)


    def test_ftp(self):
        uri = 'ftp://test.lpod-project.org/example.odt'
        container = get_odf_container(uri)



class ContainerTestCase(TestCase):

    def test_clone(self):
        container = new_odf_container(odf_class='text')
        clone = container.clone()
        self.assertEqual(clone.uri, None)


    def test_odf_xml(self):
        self.assertRaises(ValueError, get_odf_container,
                          'samples/example.xml')


    def test_get_part_xml(self):
        container = get_odf_container('samples/example.odt')
        content = container.get_part('content')
        self.assert_(isinstance(content, list))
        self.assert_(isinstance(content[0], list))


    def test_get_part_mimetype(self):
        container = get_odf_container('samples/example.odt')
        mimetype = container.get_part('mimetype')
        self.assertEqual(mimetype, ODF_EXTENSIONS['odt'])