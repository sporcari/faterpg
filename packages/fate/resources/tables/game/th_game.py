#!/usr/bin/python
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('df_fbcolumns')
        r.fieldcell('df_colswith')
        r.fieldcell('title')
        r.fieldcell('ruleset')
        r.fieldcell('gm_id')
        r.fieldcell('weekday')
        r.fieldcell('image')

    def th_order(self):
        return 'df_fbcolumns'

    def th_query(self):
        return dict(column='id', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('df_fbcolumns')
        fb.field('df_colswith')
        fb.field('title')
        fb.field('ruleset')
        fb.field('gm_id')
        fb.field('weekday')
        fb.field('image')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
