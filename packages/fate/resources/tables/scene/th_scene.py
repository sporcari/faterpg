#!/usr/bin/python
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('game_id')
        r.fieldcell('where')
        r.fieldcell('abstract')
        r.fieldcell('image')
        r.fieldcell('session_id')
        r.fieldcell('scenario_id')

    def th_order(self):
        return 'game_id'

    def th_query(self):
        return dict(column='id', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('game_id')
        fb.field('where')
        fb.field('abstract')
        fb.field('image')
        fb.field('session_id')
        fb.field('scenario_id')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
