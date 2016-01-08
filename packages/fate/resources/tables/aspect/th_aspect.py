#!/usr/bin/python
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('phrase')
        r.fieldcell('image')
        r.fieldcell('game_id')
        r.fieldcell('undiscovered')
        r.fieldcell('aspect_type_id')
        r.fieldcell('pc_id')
        r.fieldcell('npc_id')
        r.fieldcell('scene_id')
        r.fieldcell('free_invocations')
        r.fieldcell('invoke_cnt')
        r.fieldcell('compel_cnt')

    def th_order(self):
        return 'phrase'

    def th_query(self):
        return dict(column='phrase', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('phrase')
        fb.field('image')
        fb.field('game_id')
        fb.field('undiscovered')
        fb.field('aspect_type_id')
        fb.field('pc_id')
        fb.field('npc_id')
        fb.field('scene_id')
        fb.field('free_invocations')
        fb.field('invoke_cnt')
        fb.field('compel_cnt')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
