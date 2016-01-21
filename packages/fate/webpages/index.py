#!/usr/bin/env pythonw
# -*- coding: UTF-8 -*-

class GnrCustomWebPage(object):
    py_requires='pagecontent_handler/pagecontent_handler:PageContentIndex'
    def windowTitle(self):
        return 'Fate RPG webtabletop'

    def rootWidget(self, root, **kwargs):
        return root.borderContainer(_class='homelayout',**kwargs)