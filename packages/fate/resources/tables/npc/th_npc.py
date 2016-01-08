#!/usr/bin/python
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('df_fbcolumns')
        r.fieldcell('df_colswith')
        r.fieldcell('name')
        r.fieldcell('description')
        r.fieldcell('game_id')
        r.fieldcell('image')
        r.fieldcell('npc_type_id')

    def th_order(self):
        return 'df_fbcolumns'

    def th_query(self):
        return dict(column='name', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('df_fbcolumns')
        fb.field('df_colswith')
        fb.field('name')
        fb.field('description')
        fb.field('game_id')
        fb.field('image')
        fb.field('npc_type_id')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
