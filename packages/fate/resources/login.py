#!/usr/bin/env pythonw
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent

class LoginComponent(BaseComponent):

    def onUserSelected(self,avatar,data):
        if not avatar:
            return

        if avatar.authmode == 'xml':
            return

        player_tbl = self.db.table('fate.player')
        player = player_tbl.query(where='$user_id=:uid',uid=avatar.user_id).fetch()
        if not player:
            player = dict(user_id=avatar.user_id)
            player_tbl.insert(player)
            self.db.commit()
        else:
            player = player[0]
        data['player_id'] = player['id']