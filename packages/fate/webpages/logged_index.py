#!/usr/bin/env pythonw
# -*- coding: UTF-8 -*-

class GnrCustomWebPage(object):
    auth_main='user'
    py_requires='th/th:TableHandler,public:Public'

    def windowTitle(self):
        return 'Fate RPG webtabletop'

    def rootWidget(self, root, **kwargs):
        return root.borderContainer(_class='homelayout',**kwargs)
    
    def main(self,root,**kwargs):
        tc = root.tabContainer(datapath='main', region='center')
        self.playerProfile(tc.contentPane(title='Profile'))
        self.playerGames(tc.contentPane(title='Games'))
        
        tc.contentPane(title='Character Sheets')
        tc.contentPane(title='Friends')
        tc.contentPane(title='Docs')
        #first