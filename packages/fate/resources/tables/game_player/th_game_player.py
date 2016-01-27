#!/usr/bin/python
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('game_id')
        r.fieldcell('player_id')
        r.fieldcell('character_id')

    def th_order(self):
        return 'game_id'

    def th_query(self):
        return dict(column='id', op='contains', val='')

class ViewGamePlayers(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('player_id',width='15em',cellClasses='cellPlayer')
        r.cell('page_id',calculated=True,width='10em',name='Page')
        r.fieldcell('character_id',width='15em')



class ViewFromGame(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('player_id', name='Player', width='100%', edit=dict(condition='$current_player_friend IS TRUE'))
        r.fieldcell('role_desc',width='3em',name=' ')
        r.checkboxcolumn('gm', width='4em', name='GM',
                          radioButton=True, 
                          checkedField='player_id',
                          checkedId='#FORM.record.gm_id')

class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('game_id')
        fb.field('player_id')
        fb.field('character_id')

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
