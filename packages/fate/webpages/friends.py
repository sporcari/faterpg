#!/usr/bin/env pythonw
# -*- coding: UTF-8 -*-

class GnrCustomWebPage(object):
    auth_main='user'
    py_requires='th/th:TableHandler,public:Public'
    css_theme = 'fate'
    css_requires = 'css/fate'

    def windowTitle(self):
        return 'Friends'

    def main(self,root,**kwargs):
        bc = root.borderContainer(datapath='main')

        fb = bc.contentPane(region='top').formbuilder(cols=2,border_spacing='3px')
        fb.dbSelect(dbtable='fate.player',
                    lbl='Search...',
                    value='^.friend_id',
                    condition='$id!=:env_player_id AND $current_player_friend IS FALSE',
                    columns='$fullname,$nickname,$username',
                    auxColumns='$fullname,$nickname,$username')
        fb.button('Add friend', action='FIRE addFriend')
        fb.dataRpc('dummy', self.db.table('fate.friend').addFriend, friend_id='=.friend_id', _fired='^addFriend', _onResult='SET .friend_id = null;')
        bc.contentPane(region='center').plainTableHandler(table='fate.friend', view_store_onStart=True,
                                           viewResource='ViewFromPlayerDashboard',
                                           delrow=True,
                                           configurable=False)