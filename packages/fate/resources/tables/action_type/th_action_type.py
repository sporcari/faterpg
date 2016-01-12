#!/usr/bin/python
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('name')
        r.fieldcell('description')
        r.fieldcell('succeed')
        r.fieldcell('with_style')
        r.fieldcell('fail')
        r.fieldcell('tie')

    def th_order(self):
        return 'name'

    def th_query(self):
        return dict(column='name', op='contains', val='')



class Form(BaseComponent):
    css_requires='css/fate'

    def th_form(self, form):
        bc = form.center.borderContainer(datapath='.record')
        fb = bc.contentPane(region='center', margin='4px').formbuilder(cols=1, border_spacing='4px')
        fb.field('name', mandatory=True)
        fb.field('description')
        fb.field('fail', tag='simpletextarea', height='8ex')
        fb.field('tie', tag='simpletextarea', height='8ex')
        fb.field('succeed', tag='simpletextarea', height='8ex')
        fb.field('with_style', tag='simpletextarea', height='8ex')


        bc.contentPane(region='right',width='150px').div(
                                         _class='^.$cls_action')
        bc.dataFormula('.$cls_action',"code? 'action_60 action_'+code:'';",code='^.code')

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
