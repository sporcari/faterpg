#!/usr/bin/python
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('scene_id')
        r.fieldcell('npc_id')

    def th_order(self):
        return 'npc_id'

    def th_options(self):
        return dict(virtualStore=False)

class ViewFromScene(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('npc_id', name='Name', width='11em')
        r.fieldcell('@npc_id.high_concept', name='High Concept')
        r.fieldcell('@npc_id.@npc_type.name', name='Type', width='6em')
        r.fieldcell('@npc_id.mob', width='3em')
        #r.fieldcell('@npc_id.data.mob_size', editDisabled='=#ROW.mob?=!#v',  edit=dict(validate_notnull='=#ROW.mob'))

    def th_order(self):
        return 'npc_id'



class Form(BaseComponent):

    def th_form(self, form):
        form.center.borderContainer(datapath='.record')