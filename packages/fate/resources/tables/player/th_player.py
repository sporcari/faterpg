#!/usr/bin/python
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('firstname')
        r.fieldcell('lastname')
        r.fieldcell('nickname')
        r.fieldcell('user_id')
        r.fieldcell('avatar_img')

    def th_order(self):
        return 'firstname'

    def th_query(self):
        return dict(column='id', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('firstname')
        fb.field('lastname')
        fb.field('nickname')
        fb.field('user_id')
        fb.field('avatar_img')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
