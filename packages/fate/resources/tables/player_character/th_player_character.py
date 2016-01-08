#!/usr/bin/python
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('player_id')
        r.fieldcell('game_id')
        r.fieldcell('name')
        r.fieldcell('description')
        r.fieldcell('refresh')
        r.fieldcell('high_concept_id')
        r.fieldcell('trouble_id')
        r.fieldcell('fate_points')
        r.fieldcell('image')

    def th_order(self):
        return 'player_id'

    def th_query(self):
        return dict(column='name', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('player_id')
        fb.field('game_id')
        fb.field('name')
        fb.field('description')
        fb.field('refresh')
        fb.field('high_concept_id')
        fb.field('trouble_id')
        fb.field('fate_points')
        fb.field('image')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
