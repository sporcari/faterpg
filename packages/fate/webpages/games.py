#!/usr/bin/env pythonw
# -*- coding: UTF-8 -*-

class GnrCustomWebPage(object):
    auth_main='user'
    py_requires='th/th:TableHandler,public:Public'
    css_theme = 'fate'
    css_requires = 'css/fate'

    def windowTitle(self):
        return 'Games'

    def main(self,root,**kwargs):
        bc = root.borderContainer(datapath='main')        
        th = bc.contentPane(region='center').stackTableHandler(table='fate.game',
                                            view_store_onStart=True,
                                           viewResource='ViewFromPlayerDashboard',
                                           formResource='Form',pbl_classes='*',
                                           configurable=False)
        th.view.top.popNode('bar')
