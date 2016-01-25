#!/usr/bin/python
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('me_id')
        r.fieldcell('friend_id')

    def th_order(self):
        return 'me_id'

    def th_query(self):
        return dict(column='id', op='contains', val='')

class ViewFromPlayerDashboard(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('friend_fullname', width='18em')
        r.fieldcell('friend_nickname',width='18em')
        r.fieldcell('friend_username', width='10em')
        r.fieldcell('avatar_img')

    def th_condition(self):
        return dict(condition='$current_player_friend IS TRUE')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('me_id')
        fb.field('friend_id')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
