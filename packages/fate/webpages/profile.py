#!/usr/bin/env pythonw
# -*- coding: UTF-8 -*-

class GnrCustomWebPage(object):
    auth_main='user'
    py_requires='th/th:TableHandler,public:Public'
    css_theme = 'fate'
    css_requires = 'css/fate'

    def windowTitle(self):
        return 'Profile'

    def main(self,root,**kwargs):
        pane = root.borderContainer(datapath='main').contentPane(region='center', width='450px', margin='15px')
        pane.thFormHandler(table='fate.player',
                          startKey=self.rootenv['player_id'],
                          datapath='.player',
                          formResource='FormProfile')