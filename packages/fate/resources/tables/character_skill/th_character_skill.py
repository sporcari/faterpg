#!/usr/bin/python
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('skill_id')
        r.fieldcell('pc_id')
        r.fieldcell('npc_id')
        r.fieldcell('rate')

    def th_order(self):
        return 'skill_id'

    def th_query(self):
        return dict(column='id', op='contains', val='')

class ViewFromPC(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('rate', width='4em')
        r.fieldcell('skill_id', edit=True, width='100%')

    def th_order(self):
        return 'rate'

class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('skill_id')
        fb.field('pc_id')
        fb.field('npc_id')
        fb.field('rate')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
