#!/usr/bin/env pythonw
# -*- coding: UTF-8 -*-

class GnrCustomWebPage(object):
    auth_main='user'
    py_requires='th/th:TableHandler'
    css_requires = 'fate'

    def windowTitle(self):
        return 'Games'

    def main(self,root,**kwargs):
        bc = root.borderContainer(datapath='main')        
        bc.contentPane(region='center').dialogTableHandler(table='fate.game',
                                            view_store_onStart=True,
                                           viewResource='ViewFromPlayerDashboard',
                                           formResource='Form')
