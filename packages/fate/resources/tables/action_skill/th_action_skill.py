#!/usr/bin/python
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('action_type')
        r.fieldcell('skill_id')
        r.fieldcell('description')

    def th_order(self):
        return 'action_type'

class ViewFromSkill(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('action_type', edit=True, width='14em')
        r.fieldcell('description', edit=dict(tag='simpletextarea', height='10ex'), width='100%')


class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('action_type_id')
        fb.field('skill_id')
        fb.field('description')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
