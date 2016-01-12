#!/usr/bin/python
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('@skill_set.code', name='Set', width='5em')
        r.fieldcell('name', width='10em')
        r.fieldcell('description', width='100%')
        r.fieldcell('actions', width='10em')
        

    def th_order(self):
        return 'name'

    def th_options(self):
        return dict(virtualStore=False)

class Form(BaseComponent):

    def th_form(self, form):
        bc = form.center.borderContainer(datapath='.record')
        top = bc.borderContainer(region='top', height='240px')
        fb = top.contentPane(region='left', margin='4px', width='430px', margin_right='10px').formbuilder(cols=2, border_spacing='4px', width='100%', fld_width='90%')
        fb.field('name')
        fb.field('skill_set', lbl='Set')
        fb.field('description', tag='simpletextarea', colspan=2, height='140px')

        top.contentPane(region='center', datapath='#FORM').inlineTableHandler(relation='@actions',
                                                           viewResource='ViewFromSkill')

        bc.contentPane(region='center', datapath='#FORM').inlineTableHandler(relation='@stunts',
                                                           viewResource='ViewFromSkill')
        


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
