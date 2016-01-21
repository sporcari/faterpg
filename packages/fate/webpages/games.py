#!/usr/bin/env pythonw
# -*- coding: UTF-8 -*-

class GnrCustomWebPage(object):
    auth_main='user'
    py_requires='th/th:TableHandler,public:Public'
    css_requires = 'fate'

    def windowTitle(self):
        return 'Games'

    def main(self,root,**kwargs):
        bc = root.borderContainer(datapath='main')        
        bc.contentPane(region='center').stackTableHandler(table='fate.game',
                                            view_store_onStart=True,
                                           viewResource='ViewFromPlayerDashboard',
                                           #formResource='FormNewGame',
                                           form_link_event=False,
                                           grid_connect_onRowDblClick="""
                                                    var urlprefix = '/tabletop/play/';
                                                    var username = genro.getData('gnr.avatar.user');
                                                    var gamecode = this.widget.rowByIndex($1.rowIndex)['code'];
                                                    var url = urlprefix+username+'/'+gamecode;
                                                    genro.openWindow(url)""")
